import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('lex-runtime', region_name = 'us-east-1')
    response = client.post_text(
        botName='TestBot',
        botAlias='test',
        userId='300',
        inputText=event["messages"][0]["unstructured"]["text"])
        
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        "messages": [
            {
            "type": "unstructured",
            "unstructured": {
                "id": "string",
                "text": response['message'],
                "timestamp": "string"
                }
            }
        ]
    }