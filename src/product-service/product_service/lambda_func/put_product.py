import json
import os
import boto3
import traceback


def handler(event, context):
    try:
        product_data = json.loads(event['body'])

        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME')
        stocks_table = dynamodb.Table(stocks_table_name)
        products_table = dynamodb.Table(products_table_name)

        products_table.put_item(Item=product_data)
        stocks_table.put_item(
            Item={
                'product_id': product_data['id'],
                'count': 0
            }
        )

        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({
                'message': 'Product created successfully',
                'productId': product_data['id']
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
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
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "content-type": "application/json"
            },
            'body': json.dumps({'error': str(e)})
        }
