# src/handlers/deleteRequestById.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('photo-booth-app')

def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Delete request from DynamoDB based on request ID
    table.delete_item(Key={'requestId': request_id})

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request deleted successfully'})
    }
    return response
