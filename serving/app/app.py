import json
import os.path
import time

import joblib
from aws_embedded_metrics import metric_scope, MetricsLogger
from aws_embedded_metrics.config import get_config

metrics_config = get_config()
metrics_config.namespace = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", metrics_config.namespace)

# The specific env var isn't too important. What's important is that it'll be set on lambda, and local otherwise
# This speeds up unit tests; otherwise it auto-detects and tries to connect to HTTP sockets
metrics_config.environment = os.environ.get("AWS_EXECUTION_ENV", "local")


@metric_scope
def load_model(metrics: MetricsLogger):
    start_time = time.time()
    model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
    model = joblib.load(model_path)

    duration_seconds = time.time() - start_time
    metrics.put_metric("load_model.duration", duration_seconds, "Seconds")

    return model


model = load_model()


@metric_scope
def lambda_handler(event, context, metrics: MetricsLogger):
    request_body = json.loads(event["body"])
    prediction = str(model.predict([request_body["text"]])[0])

    metrics.put_metric("input.num_chars", len(request_body["text"]), "Count")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": prediction,
            "request": request_body
        })
    }
