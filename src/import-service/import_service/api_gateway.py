from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as _api,
    Stack,
)
from constructs import Construct


class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 import_products_fn: _lambda,
                 **kwargs
                 ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = _api.RestApi(self, 'ImportServiceApi', rest_api_name='Import Service')

        import_resource = api.root.add_resource('import')
        import_resource.add_method('GET', _api.LambdaIntegration(import_products_fn))
