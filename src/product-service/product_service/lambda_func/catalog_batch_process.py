import json
import os
import boto3
import uuid
import traceback

dynamodb = boto3.resource('dynamodb')
sns_client = boto3.resource('sns')

def handler(event, context):
    print("process products in batch")
    products_for_sns = []
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    for record in event['Records']:
        product_data = json.loads(record['body'])
        dynamodb = boto3.client('dynamodb', 'eu-central-1')
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        required_fields = ['title', 'price', 'count']

        for field in required_fields:
            if field not in product_data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'{field} is required'})
                }

        product_id = str(uuid.uuid4())

        product_item = {
            'Put': {
                'TableName': products_table_name,
                'Item': {
                    'id': {'S': product_id},
                    'title': {'S': product_data['title']},
                    'description': {'S': product_data.get('description', '')},
                    'price': {'N': str(product_data['price'])},
                }
            }
        }
        stock_item = {
            'Put': {
                'TableName': stocks_table_name,
                'Item': {
                    'product_id': {'S': product_id},
                    'count': {'N': str(product_data['count'])}
                }
            }
        }

        # Perform a transaction write
        dynamodb.transact_write_items(
            TransactItems=[product_item, stock_item]
        )

        sns_product = {
            'id': product_id,
            'title': product_data['title'],
            'description': product_data.get('description', ''),
            'price': product_data['price'],
            'count': product_data['count'],
        }
        products_for_sns.append(sns_product)

    sns_message = {
        'default': json.dumps({
            'message': 'Products created successfully',
            'products': products_for_sns
        })
    }
    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(sns_message),
        MessageStructure='json'
    )

    print(f"Message sent to SNS topic: {response['MessageId']}")

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
        },
        'body': json.dumps({
            'message': 'Batch processed successfully'
        })
    }
