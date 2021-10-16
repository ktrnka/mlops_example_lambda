import json
import os.path
import joblib
from aws_embedded_metrics import metric_scope, MetricsLogger

model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
model = joblib.load(model_path)


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
