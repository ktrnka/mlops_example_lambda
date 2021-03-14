from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_)

class ExampleService(core.Stack):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        handler = lambda_.DockerImageFunction(
            self,
            "ExampleDockerHandler",
            code=lambda_.DockerImageCode.from_image_asset("../app"),
            timeout=core.Duration.seconds(30),
            memory_size=2048
        )

        api = apigateway.RestApi(self, "example-cdk-api",
                  rest_api_name="Example service",
                  description="Example service in CDK/lambda")

        api_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("POST", api_integration)
