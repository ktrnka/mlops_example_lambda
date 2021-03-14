#!/usr/bin/env python3

from aws_cdk import core as cdk
from serving_example.lambda_service import ExampleService


app = cdk.App()
ExampleService(app, "ServingExampleStack")
app.synth()
