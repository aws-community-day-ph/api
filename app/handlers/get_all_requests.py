# src/handlers/getAllRequests.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('photo-booth-app')

def handler(event, context):
    # Retrieve all requests from DynamoDB
    response = table.scan()
    items = response['Items']

    body = {
        "per_request": {item['requestId']:item for item in items},
        "items": items
    }

    # Return the dictionary with statusCode and body
    return {
        "statusCode": 200,
        "body": json.dumps(body,  default=str),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
        }
    }
