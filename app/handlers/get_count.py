import boto3
import datetime

# load dynamodb resource and table
dynamodb = boto3.resource("dynamodbs")
table = dynamodb.Table("photo-booth-app")

def handler(event, context):
    try:
        # Get the current date and time
        current_datetime = datetime.now()

        # Format the date as "YYYYMMDD"
        date_today = current_datetime.strftime("%Y%m%d")

        # Query the DynamoDB table to get the current count for the date
        response = table.get_item(Key={"requestId": date_today})
        item = response.get("Item")

        count = item.get("count", 0)

        # Return a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
            },
            "body": json.dumps(
                {"message": "Counted", "count": count}
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
            "body": json.dumps(
                {"message": e.message}
            ),
        }
        return response
