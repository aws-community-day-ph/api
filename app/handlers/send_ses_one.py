# src/handlers/send_emails.py
# initial testing by aki
# Use 971604 as requestId for testing


import boto3
import json
import datetime
from jinja2 import Environment
from jinja2_s3loader import S3loader
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses")
s3 = boto3.client('s3')
table = dynamodb.Table("photo-booth-app")


def update_template(items, template_key):
    # Get access to email.html in s3
    response = s3.get_object(Bucket="photobooth-assets", Key=template_key)
    html_content = response["Body"].read().decode("utf-8")

    # Update template
    # (documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_template.html)
    reponse = ses_client.update_template(
        Template={
            "TemplateName": "photo_email_template",
            "SubjectPart": "Here's your photo booth picture!",
            "TextPart": "",
            "HtmlPart": html_content,
        }
    )
    print("Email template updated!")


def send_email(items):
    # Update template
    update_template(items, "templates/src_email_single.html")

    # Generate presigned_url
    # Replace 'your_bucket_name' and 'your_object_key' with the actual bucket name and object key.
    bucket_name = "templated-photo"
    folder = items["imagePath"]

    # Set the expiration time for the pre-signed URL (in this example, set to expire in 1 hour)
    expiration_time = datetime.timedelta(days=7)

    # Generate the pre-signed URLs
    image = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": f"{folder}/{folder}_1.png"},
        ExpiresIn=expiration_time.total_seconds(),
    )

    # TEMPLATE VARIABLES
    # From hosted images
    # Using cloudfront
    template_data = {
        "imagePath": image,
        "AWSTopLogo": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/AWS-header.png",
        "AWSMascot": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/mascot.png",
        "BottomLogo": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/bottom-footer.png",
        "Instagram": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/Instagram.png",
        "Facebook": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/Facebook.png",
        "FeedbackForm": "https://forms.gle/fahRyDJuC5SEpEJF9",
    }

    # VERIFY EMAILS
    emails = [email for email in items["emails"] if email != ""] + ["markachilesflores2004@gmail.com"]
    sent_emails = []
    failed_emails = []
    errors = []

    # SEND EMAIL
    for email in emails:
        try:
            # Using hosted images
            ses_client.send_templated_email(
                Source="awscommunityday.ph2023@gmail.com",
                Destination={"ToAddresses": [email]},
                Template="photo_email_template",
                TemplateData=json.dumps(template_data),
            )
        except ClientError as e:
            if e.response["Erorr"]["Code"] == "MessageRejected":
                print(f"Email could not be sent to {email}. Reason: {e.response['Error']['Message']}", )
            else:
                print(f"An unexpected error occurred: {e}")
            errors.append(str(e))
            failed_emails.append(e)
            continue
        sent_emails.append(email)


    print("Email sent!")
    return sent_emails, failed_emails, errors


def handler(event, context):
    # Extract request ID from path parameter
    request_id = event["pathParameters"]["requestId"]

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={"requestId": request_id})
    items = response["Item"]

    emails, failures, errors = send_email(items)

    # Update DynamoDB requestId status
    table.update_item(
        Key={"requestId": request_id},
        UpdateExpression="SET #status_attr = :status_val",
        ExpressionAttributeNames={"#status_attr": "status"},
        ExpressionAttributeValues={":status_val": "sent"},
    )

    body = {
        "requestId": request_id,
        "successful_emails": emails,
        "failed_emails": failures,
        "errors": errors,
        "body": "Email sent successfully!",
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # This allows CORS from any origin
        },
        "body": json.dumps(body),
    }

    return response
