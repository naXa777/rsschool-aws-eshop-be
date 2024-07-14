from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as _api,
    Stack,
)
from constructs import Construct


class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 import_products_fn: _lambda,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        basic_auth_lambda = _lambda.Function.from_function_name(self, "authFunction", "AuthFunction")

        api = _api.RestApi(
            self, 'ImportServiceApi',
            default_cors_preflight_options={
                "allow_origins": _api.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": _api.Cors.DEFAULT_HEADERS,
            },
            rest_api_name='Import Service'
        )
        authorizer = _api.TokenAuthorizer(
            self, 'BasicAuthorizer',
            handler=basic_auth_lambda,
            identity_source='method.request.header.Authorization'
        )
        api.add_gateway_response(
            "UnauthorizedResponse",
            type=_api.ResponseType.UNAUTHORIZED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                "Access-Control-Allow-Methods": "'GET, POST, PUT, DELETE, OPTIONS'",
            },
            status_code="401",
            templates={
                "application/json": '{"message": "Unauthorized"}'
            },
        )
        api.add_gateway_response(
            "AccessForbiddenResponse",
            type=_api.ResponseType.ACCESS_DENIED,
            response_headers={
                "Access-Control-Allow-Origin": "'*'",
                "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                "Access-Control-Allow-Methods": "'GET, POST, PUT, DELETE, OPTIONS'",
            },
            status_code="403",
            templates={
                "application/json": '{"message": "Access Forbidden"}'
            },
        )

        import_resource = api.root.add_resource('import')
        import_resource.add_method(
            'GET',
            _api.LambdaIntegration(import_products_fn),
            authorization_type=_api.AuthorizationType.CUSTOM,
            authorizer=authorizer
        )
