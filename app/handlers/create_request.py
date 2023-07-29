# src/handlers/createRequest.py
# pushed sample


import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")


def generate_request_id():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date as "YYYYMMDD"
    date_today = current_datetime.strftime("%Y%m%d")

    # Query the DynamoDB table to get the current count for the date
    response = table.get_item(Key={"requestId": date_today})
    item = response.get("Item")

    # If no item exists for the date, start the count at 1
    if item is None:
        count = 1
    else:
        count = item.get("count", 0) + 1

    # Update the count for the date in the DynamoDB table
    table.put_item(Item={"requestId": date_today, "count": count})

    # Generate the requestId using the format R-datetoday-count
    request_id = f"R-{date_today}-{count:03}"

    return request_id


def handler(event, context):
    try:
        # Parse request body
        request_body = json.loads(event["body"])

        # Extract data from request body
        emails = request_body["emails"]

        # Generate the requestId
        request_id = generate_request_id()

        # Save the request to DynamoDB
        table.put_item(
            Item={
                "requestId": request_id,
                "emails": emails,
                "imagePath": "",
                "status": "pending"
            }
        )

        # Return a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
            },
            "body": json.dumps(
                {"message": "Request created successfully", "requestId": request_id}
            ),
        }
        return response

    except Exception as e:
         # Return a response
        response = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
            },
            "body": json.dumps({"message": str(e)}),
        }
    