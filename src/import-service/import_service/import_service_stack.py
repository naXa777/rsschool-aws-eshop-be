from aws_cdk import Stack
from import_service.api_gateway import ApiGateway
from import_service.import_products import ImportProducts
from import_service.parse_products import ParseProducts
from constructs import Construct

class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = 'rsschool-import-bucket-aws-2024'

        import_products_lambda = ImportProducts(self, 'ImportLambda', bucket_name)
        ParseProducts(self, 'ParseLambda', bucket_name)
        ApiGateway(self, 'API_Gateway', import_products_fn=import_products_lambda.import_products)
