# src/handlers/getRequestById.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('photo-booth-app')

def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={'requestId': request_id})
    item = response['Item']

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    return response
