import pytest
from moto import mock_aws
import boto3
from import_service.lambda_func import import_file

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
        yield s3

def test_handler(s3_setup):
    event = {
        "queryStringParameters": {"name": "test.csv"}
    }
    context = {}
    response = import_file.handler(event, context)
    assert response['statusCode'] == 200
    assert 'https://test-bucket.s3.amazonaws.com/uploaded/test.csv' in response['body']
