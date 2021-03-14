from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_)

class ExampleService(core.Stack):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        bucket = s3.Bucket(self, "ExampleServiceStorage")

        handler = lambda_.Function(self, "ExampleServiceHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.from_asset("resources"),
                    handler="app.lambda_handler",
                    environment=dict(
                        BUCKET=bucket.bucket_name)
                    )

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "example-cdk-api",
                  rest_api_name="Example service",
                  description="Example service in CDK/lambda")

        api_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", api_integration)   # GET /
