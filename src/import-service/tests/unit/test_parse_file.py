import pytest
from moto import mock_aws
import boto3
from botocore.exceptions import ClientError
from import_service.lambda_func import parse_file

@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    """Mock AWS credentials for moto to avoid using actual AWS accounts."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("BUCKET_NAME", 'test-bucket')

@pytest.fixture
def s3_setup():
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='uploaded/test.csv', Body="product,price\nAmber,30\nBurn,25")
        yield s3

@mock_aws
def test_parse_file_handler(s3_setup):
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
    assert parsed_content == "product,price\nAmber,30\nBurn,25", "Content mismatch after parsing"

    # Check if original file is deleted
    try:
        s3_resource.Object('test-bucket', 'uploaded/test.csv').load()
        assert False, "The file still exists; it should have been deleted."
    except ClientError:
        print("ok")
