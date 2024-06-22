from aws_cdk import Stack
from product_service.api_gateway import ApiGateway
from product_service.get_product_by_id import ProductById
from product_service.get_products import GetProducts
from constructs import Construct


class MyCdkProductServiceAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines my stack goes here
        get_products_list_lambda = GetProducts(self, 'ProductsList')
        get_product_by_id_lambda = ProductById(self, 'ProductById')
        ApiGateway(self, 'APIGateway',
                   get_products_list_fn=get_products_list_lambda.get_products_list,
                   get_product_by_id_fn=get_product_by_id_lambda.get_product_by_id,
                   )
