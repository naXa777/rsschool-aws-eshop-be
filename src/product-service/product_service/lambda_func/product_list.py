import json


def handler(event, context):

    products = [
        {"id": "1", "title": "Coffee Mug \"DevOps\"",
         "description": "Tell me, this DevOps is just a buzzword, isn't it?", "price": 15},
        {"id": "2", "title": "Men's T-shirt \"Sarcasm DevOps Software Development\"", "price": 79},
        {"id": "3", "title": "WHITE MUG WITH PRINT",
         "description": "✅ Are you looking for the perfect gift?\n✔️ Here's the perfect idea - our mug!", "price": 12},
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
