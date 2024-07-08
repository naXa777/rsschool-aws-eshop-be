import json
import sys
import os
import boto3
from moto import mock_aws
import pytest

lambda_dir = os.path.dirname('../../product_service/lambda_func')
sys.path.append(lambda_dir)
from product_service.lambda_func import product_by_id

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

        # Insert mock data
        dynamodb.put_item(
            TableName='products',
            Item={
                'id': {'S': '1'},
                'title': {'S': 'Coffee Mug "DevOps"'},
                'description': {'S': 'Description 1'},
                'price': {'N': '15'}
            }
        )

        dynamodb.put_item(
            TableName='stocks',
            Item={
                'product_id': {'S': '1'},
                'count': {'N': '1'}
            }
        )

        yield dynamodb

def test_handler_returns_product(aws_setup):
    event = {
        'pathParameters': {
            'productId': '1'
        }
    }
    response = product_by_id.handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['title'] == 'Coffee Mug "DevOps"'
    assert body['price'] == 15
    assert body['count'] == 1


def test_handler_returns_404_for_non_existent_product(aws_setup):
    event = {
        'pathParameters': {
            'productId': '404'
        }
    }
    response = product_by_id.handler(event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body['message'] == 'Product not found'


if __name__ == '__main__':
    pytest.main()
