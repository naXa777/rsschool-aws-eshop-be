import pytest
from moto import mock_aws
import boto3
import os
from botocore.exceptions import ClientError
from import_service.lambda_func import parse_file


@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    """Mock AWS credentials for moto to avoid using actual AWS accounts."""
    # monkeypatch.setenv("AWS_REGION", "eu-central-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("BUCKET_NAME", 'test-bucket')


@pytest.fixture
def aws_setup():
    with mock_aws():
        # Mock S3
        s3 = boto3.client('s3', region_name='eu-central-1')
        s3.create_bucket(
            Bucket='test-bucket',
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-central-1'
            }
        )

        csv_file = 'title,description,price,count\nNew Test,Easy to find!,99,1'
        print(f"file content {csv_file}")
        s3.put_object(
            Bucket='test-bucket',
            Key='uploaded/test.csv',
            Body=csv_file
        )

        # Mock SQS
        sqs = boto3.client('sqs', region_name='eu-central-1')
        queue_url = sqs.create_queue(QueueName='catalogItemsQueue')['QueueUrl']
        queue_arn = sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=['QueueArn']
        )['Attributes']['QueueArn']

        os.environ['SQS_QUEUE_URL'] = queue_url
        os.environ['SQS_QUEUE_ARN'] = queue_arn

        yield s3, sqs


@mock_aws
def test_parse_file_handler(aws_setup):
    # Arrange
    # a mock event that mimics the AWS S3 put event
    event = {
        'Records': [{
            's3': {
                'bucket': {
                    'name': 'test-bucket'
                },
                'object': {
                    'key': 'uploaded/test.csv'
                }
            }
        }]
    }
    context = {}

    # Act
    parse_file.handler(event, context)

    # Assert
    s3_resource = boto3.resource('s3')
    parsed_obj = s3_resource.Object('test-bucket', 'parsed/test.csv')
    parsed_content = parsed_obj.get()['Body'].read().decode('utf-8')

    # Check if file was copied
    expected_content = 'title,description,price,count\nNew Test,Easy to find!,99,1'
    assert parsed_content == expected_content, "Content mismatch after parsing"

    # Check if original file is deleted
    try:
        s3_resource.Object('test-bucket', 'uploaded/test.csv').load()
        assert False, "The file still exists; it should have been deleted."
    except ClientError:
        print("ok")
