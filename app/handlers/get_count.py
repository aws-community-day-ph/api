import boto3
import json
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")

def handler(event, context):
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date as "YYYYMMDD"
    date_today = current_datetime.strftime('%Y%m%d')

    # Get the necessary record from database using date_today as value
    # Replace '20230716' with date_today
    response = table.get_item(Key={'requestId': '20230716'})
    item = response.get('Item')

    # Get count from the database in dynamodb
    count = item.get('count')
    print(type(count))

    # Return the result from dynamodb
    body = {
        'count': int(count)
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response
