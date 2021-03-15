from aws_cdk import (core as cdk,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_)

class TextClassifierService(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str):
        super().__init__(scope, id)

        handler = lambda_.DockerImageFunction(
            self,
            "ExampleTextClassifierHandler",
            code=lambda_.DockerImageCode.from_image_asset("../app"),
            timeout=cdk.Duration.seconds(60),
            memory_size=3008
        )

        api = apigateway.RestApi(
            self,
            "ExampleTextClassifierApi",
            rest_api_name="Example text classifier service",
            description="Example text classifier service"
        )

        api_integration = apigateway.LambdaIntegration(
            handler,
            # I'm not sure if this is needed; I copied it from an example
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method("POST", api_integration)
