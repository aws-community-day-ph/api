# src/handlers/updateRequestById.py

import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")

def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']
    status = event["pathParameters"]["status"]

    # Update request in DynamoDB based on request ID
    table.update_item(
        Key={
            'requestId': request_id 
        },
        UpdateExpression='SET #status_attr = :status_val',
        ExpressionAttributeNames={
            '#status_attr': 'status'
        },
        ExpressionAttributeValues={
            ':status_val': status
        }
    )

    # Return a response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request updated successfully'})
    }
    return response
