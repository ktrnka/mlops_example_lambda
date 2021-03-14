#!/usr/bin/env python3

from aws_cdk import core as cdk
from serving_example.lambda_service import TextClassifierService


app = cdk.App()
TextClassifierService(app, "ExampleTextClassifierStack")
app.synth()
