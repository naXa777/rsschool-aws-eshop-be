import os
import csv
import io
import boto3
import traceback

s3 = boto3.client('s3')


def handler(event, context):
    print("parse file from S3")

    bucket_name = os.environ['BUCKET_NAME']

    for record in event['Records']:
        key = record['s3']['object']['key']
        print(f'parsing file {key}')

        response = s3.get_object(Bucket=bucket_name, Key=key)
        body = response['Body']

        csv_file = io.StringIO(body.read().decode('utf-8'))
        reader = csv.DictReader(csv_file)

        print('File rows:')
        for row in reader:
            print(row)

        copy_source = {'Bucket': bucket_name, 'Key': key}
        parsed_key = key.replace('uploaded/', 'parsed/')
        s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=parsed_key)

        if key != 'uploaded/':
            print(f'deleting {key}')
            s3.delete_object(Bucket=bucket_name, Key=key)
