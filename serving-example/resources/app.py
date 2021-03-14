import json

def lambda_handler(event, context):
    print(f"event: {event}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }