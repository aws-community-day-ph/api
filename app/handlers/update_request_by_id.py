# src/handlers/updateRequestById.py

import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")

def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Parse request body
    request_body = json.loads(event['body'])

    # Extract image path from request body
    imagePath = request_body["imagePath"]
    status = request_body["status"]

    # Update imagePath and status
    table.update_item(
        Key={
            'requestId': request_id 
        },
        UpdateExpression='SET imagePath = :imagePath, #status_attr = :status_val',
        ExpressionAttributeNames={
            '#status_attr': 'status'
        },
        ExpressionAttributeValues={
            ':imagePath': imagePath,
            ':status_val': status
        }
    )

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request updated successfully'})
    }
    return response
