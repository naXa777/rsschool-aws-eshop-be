from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    Stack,
)
from constructs import Construct


class ImportProducts(Stack):

    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(self, "ImportBucket", bucket_name)

        self.import_products = _lambda.Function(
            self, 'ImportProductsHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='import_file.handler',
            code=_lambda.Code.from_asset('import_service/lambda_func/'),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        bucket.grant_put(self.import_products)
        bucket.grant_read_write(self.import_products)
