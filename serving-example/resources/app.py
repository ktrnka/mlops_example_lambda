import json
import os.path
import joblib

model_path = os.path.join(os.path.dirname(__file__), "data/model.joblib.gz", )
model = joblib.load(model_path)

def lambda_handler(event, context):
    post_body = json.loads(event["body"])
    prediction = str(model.predict([post_body["text"]])[0])

    return {
        'statusCode': 200,
        'body': json.dumps({
            "response": prediction,
            "request": post_body
        })
    }