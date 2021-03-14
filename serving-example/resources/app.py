import json

def lambda_handler(event, context):
    post_body = json.loads(event["body"])

    return {
        'statusCode': 200,
        'body': json.dumps({
            "response": f"Hello from Lambda, I see you said {post_body['text']}",
            "request": event
        })
    }