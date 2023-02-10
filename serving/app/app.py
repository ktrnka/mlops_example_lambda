import json
import os.path
import time
from datetime import datetime

import joblib
from aws_embedded_metrics import metric_scope, MetricsLogger
from aws_embedded_metrics.config import get_config


class EmfMetrics:
    """Cloudwatch Embedded Metrics Format (EMF) for custom metrics"""
    @staticmethod
    def setup():
        metrics_config = get_config()
        metrics_config.namespace = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", metrics_config.namespace) + "_emf"

        # This speeds up unit tests; otherwise it auto-detects and tries to connect to HTTP sockets
        metrics_config.environment = os.environ.get("AWS_EXECUTION_ENV", "local")

    @staticmethod
    @metric_scope
    def put_duration(name: str, duration_seconds: float, metrics: MetricsLogger):
        metrics.put_metric(name, duration_seconds, "Seconds")

    @staticmethod
    @metric_scope
    def put_count(name: str, count: int, metrics: MetricsLogger):
        metrics.put_metric(name, count, "Count")



def load_model():
    start_time = time.time()
    model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
    model = joblib.load(model_path)

    duration_seconds = time.time() - start_time

    # TODO: Replace this with a function decorator that computes the duration for you
    EmfMetrics.put_duration("load_model.duration", duration_seconds)

    return model


EmfMetrics.setup()
model = load_model()


def lambda_handler(event, context):
    request_body = json.loads(event["body"])
    prediction = model.predict([request_body["text"]])[0]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": prediction,
            "request": request_body
        })
    }
