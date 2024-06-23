import boto3
import uuid6
import json
import random


dynamodb = boto3.resource('dynamodb')

products_table = dynamodb.Table('products')
stocks_table = dynamodb.Table('stocks')

def populate_tables(items):

    for item in items:
        product_id = str(uuid6.uuid7())
        title = item['title']
        description = item.get('description')
        price = item.get('price')
        count = random.randint(1, 10)

        products_table.put_item(
            Item={
                'id': product_id,
                'title': title,
                'description': description,
                'price': price,
            }
        )

        stocks_table.put_item(
            Item={
                'product_id': product_id,
                'count': count
            }
        )

with open('products-data.json', 'r') as json_file:
    data = json.load(json_file)

populate_tables(data)
