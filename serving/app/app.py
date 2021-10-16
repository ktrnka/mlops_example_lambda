import json
import os.path
import time

import joblib
from aws_embedded_metrics import metric_scope, MetricsLogger
from aws_embedded_metrics.config import get_config


class EmfMetrics:
    @staticmethod
    def setup():
        metrics_config = get_config()
        metrics_config.namespace = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", metrics_config.namespace)

        # This speeds up unit tests; otherwise it auto-detects and tries to connect to HTTP sockets
        metrics_config.environment = os.environ.get("AWS_EXECUTION_ENV", "local")

    @metric_scope
    @staticmethod
    def put_duration(name: str, duration_seconds: float, metrics: MetricsLogger):
        metrics.put_metric(name, duration_seconds, "Seconds")

    @metric_scope
    @staticmethod
    def put_count(name: str, count: int, metrics: MetricsLogger):
        metrics.put_metric(name, count, "Count")


@metric_scope
def load_model(metrics: MetricsLogger):
    start_time = time.time()
    model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
    model = joblib.load(model_path)

    duration_seconds = time.time() - start_time
    EmfMetrics.put_duration("load_model.duration", duration_seconds)

    return model


model = load_model()


@metric_scope
def lambda_handler(event, context, metrics: MetricsLogger):
    request_body = json.loads(event["body"])
    prediction = str(model.predict([request_body["text"]])[0])

    EmfMetrics.put_count("input.num_chars", len(request_body["text"]))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": prediction,
            "request": request_body
        })
    }
