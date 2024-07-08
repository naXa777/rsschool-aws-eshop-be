import json
import sys
import os
import boto3
from moto import mock_aws
import pytest

lambda_dir = os.path.dirname('../../product_service/lambda_func')
sys.path.append(lambda_dir)
from product_service.lambda_func import catalog_batch_process

@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    """Mock AWS credentials for moto to avoid using actual AWS accounts."""
    monkeypatch.setenv("AWS_REGION", "eu-central-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("STOCKS_TABLE_NAME", "stocks")
    monkeypatch.setenv("PRODUCTS_TABLE_NAME", "products")

@pytest.fixture
def aws_setup():
    with mock_aws():
        # Mock DynamoDB
        dynamodb = boto3.client('dynamodb', region_name='eu-central-1')

        # Create tables
        dynamodb.create_table(
            TableName='products',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 2}
        )
        dynamodb.create_table(
            TableName='stocks',
            KeySchema=[{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 2}
        )

        # Mock SNS
        sns = boto3.client('sns', region_name='eu-central-1')
        topic_arn = sns.create_topic(Name='createProductTopic')['TopicArn']
        os.environ['SNS_TOPIC_ARN'] = topic_arn

        yield dynamodb, sns

@pytest.fixture
def lambda_event():
    return {
        "Records": [
            {
                "body": json.dumps({
                    "title": "Test Product",
                    "description": "How Much?",
                    "price": 99,
                    "count": 9
                })
            }
        ]
    }

def test_handler_missing_fields(lambda_event, aws_setup):
    incomplete_event = {
        "Records": [
            {
                "body": json.dumps({
                    "title": "Test Product",
                    "description": "Malformed product",
                })
            }
        ]
    }

    response = catalog_batch_process.handler(incomplete_event, None)

    assert response['statusCode'] == 400
    assert 'error' in json.loads(response['body'])

def test_handler_success(lambda_event, aws_setup):
    dynamodb, sns = aws_setup

    response = catalog_batch_process.handler(lambda_event, None)

    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'message': 'Batch processed successfully'}

    # Check if items are written to the DynamoDB tables
    products_response = dynamodb.scan(TableName='products')
    stocks_response = dynamodb.scan(TableName='stocks')

    assert len(products_response['Items']) == 1
    assert len(stocks_response['Items']) == 1

    # Check if message was published to SNS
    topics = sns.list_topics()
    assert len(topics['Topics']) == 1

if __name__ == '__main__':
    pytest.main()
