import os
import boto3
import json
import traceback

s3 = boto3.client('s3')

def handler(event, context):
    print("GET /import request. Query parameters:", event.get('queryStringParameters'))

    try:
        if event['queryStringParameters'] is None or 'name' not in event.get("queryStringParameters", {}):
            raise ValueError("name is a required parameter")
        file_name = event["queryStringParameters"]["name"]
        if not file_name:
            raise ValueError("name should not be empty")
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

    except ValueError as e:
        return {
            'statusCode': 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }

    except Exception as e:
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }
