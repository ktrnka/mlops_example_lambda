#!/usr/bin/env python3

from aws_cdk import core as cdk
from stacks.lambda_service import TextClassifierService


app = cdk.App()
TextClassifierService(app, "ExampleTextClassifierStack")
app.synth()
