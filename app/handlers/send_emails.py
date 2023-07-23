# src/handlers/send_emails.py
# initial testing by aki
# Use 971604 as requestId for testing


import boto3
import json

dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses")
s3 = boto3.client("s3")
table = dynamodb.Table("photo-booth-app")


def update_template(items):
    # Get access to email.html in s3
    response = s3.get_object(Bucket='photobooth-assets', Key='templates/email.html')
    html_content = response['Body'].read().decode('utf-8')

    # Update template
    # (documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_template.html)
    reponse = ses_client.update_template(
        Template={
            "TemplateName": "photo_email_template",
            "SubjectPart": "Here's your photo booth picture!",
            "TextPart": "",
            "HtmlPart": html_content
        }
    )
    print("Email template updated!")


def send_email(items):
    # Variable values for email template
    template_data = {
        'imagePath': items['imagePath'],
        "AWSTopLogo": "https://photobooth-assets.s3.ap-southeast-1.amazonaws.com/templates/assets/AWSMascot.svg/AWSTopLogo.svg",
        "AWSMascot": "https://photobooth-assets.s3.ap-southeast-1.amazonaws.com/templates/assets/AWSMascot.svg/AWSMascot.svg",
        "BottomLogo": "https://photobooth-assets.s3.ap-southeast-1.amazonaws.com/templates/assets/AWSMascot.svg/BottomLogo.svg",
        "Instagram": "https://photobooth-assets.s3.ap-southeast-1.amazonaws.com/templates/assets/AWSMascot.svg/Instagram.svg",
        "Facebook": "https://photobooth-assets.s3.ap-southeast-1.amazonaws.com/templates/assets/AWSMascot.svg/Facebook.svg"
    }

    # Send email
    ses_client.send_templated_email(
        Source = 'anthony.basang18@gmail.com',
        Destination = {
            'ToAddresses': items['emails']
        },
        ReplyToAddresses = ['anthony.basang18@gmail.com'],
        Template = 'photo_email_template',
        TemplateData = json.dumps(template_data)
    )
    print("Email sent!")


def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={'requestId': request_id})
    items = response['Item']

    update_template(items)
    send_email(items)

    body = {
        "body": "Email sent!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
