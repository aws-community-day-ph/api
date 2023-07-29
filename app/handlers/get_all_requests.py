import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("photo-booth-app")

def handler(event, context):
    response = table.scan()
    items = response['Items']
    print("items eto", items)

    # Create a dictionary to group records by a unique identifier (group_id)
    grouped_records = {}
    for item in items:
        if 'count' in item:
            group_id = item['requestId']
        else:
            group_id = item['requestId']
        if group_id not in grouped_records:
            grouped_records[group_id] = []
        grouped_records[group_id].append(item)

    # Extract the counts for each group
    counts = {k: len(v) for k, v in grouped_records.items() if 'count' not in k}

    response = {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
        },
        'body': json.dumps({
            'requests': [item for item in items if 'count' not in item],
            'counts': counts
        }, default=str)
    }
    return response
