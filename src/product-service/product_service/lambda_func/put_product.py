import json
import os
import boto3
import traceback
import uuid


def handler(event, context):
    print("POST /product request. Body: %s", event.get('body'))

    try:
        product_data = json.loads(event['body'])

        if not isinstance(product_data['title'], str):
            raise ValueError("Expected type for 'title': string.")
        if not isinstance(product_data['price'], int):
            raise ValueError("Expected type for 'price': integer.")
        if product_data['price'] < 0:
            raise ValueError("'price' cannot be negative.")
        if not isinstance(product_data.get('description', ''), str):
            raise ValueError("Expected type for 'description': string.")
        if not isinstance(product_data['count'], int):
            raise ValueError("Expected type for 'count': integer.")
        if product_data['count'] < 0:
            raise ValueError("'count' cannot be negative.")

        dynamodb = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')

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

        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({
                'message': 'Product created successfully',
                'productId': product_id
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({'error': f'Missing key in input: {str(e)}'})
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
