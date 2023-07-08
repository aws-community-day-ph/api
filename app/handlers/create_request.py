# src/handlers/createRequest.py

import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-dynamodb-table')

def handler(event, context):
    # Parse request body
    request_body = json.loads(event['body'])

    # Extract data from request body
    emails = request_body['emails']
    image_path = request_body['image_path']
    request_id = request_body['request_id']
    status = request_body['status']

    # Save the request to DynamoDB
    table.put_item(
        Item={
            'requestId': request_id,
            'emails': emails,
            'imagePath': image_path,
            'status': status
        }
    )

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request created successfully'})
    }
    return response
