import json
import os
import boto3
import traceback


def handler(event, context):
    try:
        product_id = event["pathParameters"]["productId"]

        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
        stocks_table = dynamodb.Table(stocks_table_name)
        products_table = dynamodb.Table(products_table_name)

        # Retrieve the specific items from DynamoDB
        stocks_item = stocks_table.get_item(Key={'product_id': product_id})
        products_item = products_table.get_item(Key={'id': product_id})

        if 'Item' in products_item and 'Item' in stocks_item:
            product = {
                'id': products_item['Item']['id'],
                'title': products_item['Item']['title'],
                'description': products_item['Item'].get('description'),
                'price': str(products_item['Item'].get('price')),
                'count': str(stocks_item['Item'].get('count'))
            }
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "content-type": "application/json"
                },
                "body": json.dumps(product)
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "content-type": "application/json"
                },
                "body": json.dumps({"message": "Product not found"})
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
