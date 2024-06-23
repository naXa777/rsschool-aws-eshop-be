import json
import os
import boto3


def handler(event, context):
    try:
        product_id = event["pathParameters"]["productId"]

        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
        stocks_table = dynamodb.Table(stocks_table_name)
        products_table = dynamodb.Table(products_table_name)
        stocks_response = stocks_table.scan()
        stocks_item = stocks_response.get_item(Key={'product_id': product_id})
        products_response = products_table.scan()
        #        products_items = products_response.get('Items', [product_id])
        products_item = products_response.get_item(Key={'id': product_id})

        if products_item and stocks_item:
            product = {
                'id': products_item['id'],
                'title': products_item['title'],
                'description': products_item.get('description'),
                'price': products_item.get('price'),
                'count': stocks_item.get('count')
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
        return {
            'statusCode': 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }
