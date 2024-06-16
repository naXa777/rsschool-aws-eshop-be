import json

def handler(event, context):

    products = [
            {"id": "1", "name": "Product 1", "price": 100},
            {"id": "2", "name": "Product 2", "price": 200},
            {"id": "3", "name": "Product 3", "price": 300},
        ]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "content-type": "application/json"
        },
        "body": json.dumps(products)
    }
