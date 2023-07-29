# src/handlers/send_emails.py
# initial testing by aki
# Use 971604 as requestId for testing


import boto3
import json
import smtplib
import datetime
from email.mime.text import MIMEText
from jinja2 import Environment
from jinja2_s3loader import S3loader

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")
ses_client = boto3.client("ses")
s3 = boto3.client("s3")


def generate_template(items):
    # Generate presigned_url
    # Replace 'your_bucket_name' and 'your_object_key' with the actual bucket name and object key.
    bucket_name = "templated-photo"
    object_key = items["imagePath"]

    # Set the expiration time for the pre-signed URL (in this example, set to expire in 1 hour)
    expiration_time = datetime.timedelta(days=7)

    # Generate the pre-signed URL
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration_time.total_seconds(),
    )

    template_data = {
        "imagePath": presigned_url,
        "AWSTopLogo": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/AWS-header.png",
        "AWSMascot": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/mascot.png",
        "BottomLogo": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/bottom-footer.png",
        "Instagram": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/Instagram.png",
        "Facebook": "https://d1w8smu7unswjj.cloudfront.net/templates/assets/Facebook.png",
        "FeedbackForm": "https://forms.gle/fahRyDJuC5SEpEJF9",
    }
    # Create an environment
    env = Environment(loader=S3loader("photobooth-assets", "templates"))

    # Create the template
    template = env.get_template("src_email.html")

    return template.render(template_data)


def send_email_python(items):
    # Extablish a connection
    sender_email = "awscommunityday.ph2023@gmail.com"
    sender_app_pass = "qejqwdnktjqissmq"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email, sender_app_pass)

        # Generate template
        msg = MIMEText(generate_template(items), "html")
        msg["Subject"] = "Here's your photo booth picture!"
        msg["From"] = sender_email
        msg["To"] = ", ".join(items["emails"])

        # Send email
        smtp.sendmail(sender_email, items["emails"], msg.as_string())


def handler(event, context):
    # Extract request ID from path parameter
    request_id = event["pathParameters"]["requestId"]

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={"requestId": request_id})
    items = response["Item"]

    send_email_python(items)

    # Update DynamoDB requestId status
    table.update_item(
        Key={"requestId": request_id},
        UpdateExpression="SET #status_attr = :status_val",
        ExpressionAttributeNames={"#status_attr": "status"},
        ExpressionAttributeValues={":status_val": "sent"},
    )

    body = {
        "requestId": request_id,
        "emails": items["emails"],
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
