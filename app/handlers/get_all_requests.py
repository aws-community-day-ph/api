# src/handlers/getAllRequests.py

import json
import boto3
from aws_lambda_powertools.event_handler import Response, content_types

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('photo-booth-app')

def handler(event, context):
    # Retrieve all requests from DynamoDB
    response = table.scan()
    items = response['Items']

    # Return a response

    return Response(
        status_code=200,
        content_type=content_types.APPLICATION_JSON,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        body=json.dumps({ 
            "success": True,
            "status": "success",
            "message": items
        
    }),
)
