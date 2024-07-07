import os
import csv
import io
import boto3
import json
import traceback

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def handler(event, context):
    print("parse file from S3")

    bucket_name = os.environ['BUCKET_NAME']
    response = sqs.get_queue_url(QueueName='catalogItemsQueue')
    queue_url = response['QueueUrl']

    for record in event['Records']:
        key = record['s3']['object']['key']
        print(f'parsing file {key}')

        response = s3.get_object(Bucket=bucket_name, Key=key)
        body = response['Body']

        csv_file = io.StringIO(body.read().decode('utf-8'))
        reader = csv.DictReader(csv_file)

        for row in reader:
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(row)
            )

        copy_source = {'Bucket': bucket_name, 'Key': key}
        parsed_key = key.replace('uploaded/', 'parsed/')
        s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=parsed_key)

        if key != 'uploaded/':
            print(f'deleting {key}')
            s3.delete_object(Bucket=bucket_name, Key=key)
