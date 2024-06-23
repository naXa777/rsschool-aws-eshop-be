from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as _api,
    Stack,
)
from constructs import Construct


class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 get_products_list_fn: _lambda,
                 get_product_by_id_fn: _lambda,
                 put_products_fn: _lambda,
                 **kwargs
                 ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = _api.RestApi(self, 'ProductServiceApi', rest_api_name='Product Service')

        products_resource = api.root.add_resource('products')
        products_resource.add_method('GET', _api.LambdaIntegration(get_products_list_fn))
        products_resource.add_method('POST', _api.LambdaIntegration(put_products_fn))

        product_by_id_resource = products_resource.add_resource('{productId}')
        product_by_id_resource.add_method('GET', _api.LambdaIntegration(get_product_by_id_fn))
