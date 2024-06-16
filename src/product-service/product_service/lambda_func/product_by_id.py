import json

def handler(event, context):

    products = [
            {"id": "1", "name": "Product 1", "price": 100},
            {"id": "2", "name": "Product 2", "price": 200},
            {"id": "3", "name": "Product 3", "price": 300},
        ]
    product_id = event["pathParameters"]["productId"]
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
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
