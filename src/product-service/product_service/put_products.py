from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct


class PutProducts(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.put_products = _lambda.Function(
            self, 'CreateProductHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            handler='put_product.handler',
            environment=environment
        )
