import json
import os
import boto3
import traceback
import uuid


def handler(event, context):
    try:
        product_data = json.loads(event['body'])

        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
        stocks_table = dynamodb.Table(stocks_table_name)
        products_table = dynamodb.Table(products_table_name)

        product_entity = {
            'id': str(uuid.uuid4()),
            'title': product_data['title'],
            'description': product_data.get('description'),
            'price': product_data['price'],
        }

        products_table.put_item(Item=product_entity)
        stocks_table.put_item(
            Item={
                'product_id': product_entity['id'],
                'count': product_data['count']
            }
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
                'productId': product_entity['id']
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
