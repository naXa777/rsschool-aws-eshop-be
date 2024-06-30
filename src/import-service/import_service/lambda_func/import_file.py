import os
import boto3
import traceback

s3 = boto3.client('s3')

def handler(event, context):
    print("import file from S3")

    file_name = event["queryStringParameters"]["name"]
    bucket_name = os.environ['BUCKET_NAME']
    key = f"uploaded/{file_name}"

    params = {
        'Bucket': bucket_name,
        'Key': key,
    }

    signed_url = s3.generate_presigned_url('put_object', Params=params)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "text/plain"
        },
        "body": signed_url
    }
