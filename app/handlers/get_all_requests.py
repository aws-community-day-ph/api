# src/handlers/getAllRequests.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-dynamodb-table')

def handler(event, context):
    # Retrieve all requests from DynamoDB
    response = table.scan()
    items = response['Items']

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'requests': items})
    }
    return response
