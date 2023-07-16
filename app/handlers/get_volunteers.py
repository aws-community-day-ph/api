import csv
import boto3
import json

from collections import defaultdict

s3_client = boto3.client("s3")


def handler(event, context):
    # Retrieve the CSV file from S3
    bucket_name = "aws-community-day-assets"
    folder_path = "volunteers_data/"
    file_key = folder_path + "volunteers_data.csv"
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    print(file_obj)
    file_content = file_obj["Body"].read().decode("latin-1")

    # Group the entries by committee
    committees = defaultdict(list)
    csv_data = csv.reader(file_content.splitlines())
    headers = next(csv_data)  # Read the header row
    for row in csv_data:
        committee = row[3]
        committees[committee].append(
            {
                "email_address": row[0],
                "complete_name": row[1],
                "image_path": row[2],
                "comittee": row[3],
                "role": row[4],
                "linkedin": row[5],
                "facebook": row[6],
                "twitter": row[7],
                "instagram": row[8],
            }
        )

    # Convert the grouped data to JSON
    grouped_data = json.dumps(committees, indent=4)

    # Return the grouped data as the response
    return {
        "statusCode": 200,
        "body": grouped_data,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
