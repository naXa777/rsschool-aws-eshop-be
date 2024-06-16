from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct


class ProductById(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.get_product_by_id = _lambda.Function(
            self, 'GetProductByIdHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            handler='product_by_id.handler'
        )
