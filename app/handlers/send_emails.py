# src/handlers/send_emails.py
# initial testing by aki
# Use 971604 as requestId for testing


import boto3
import json
from jinja2 import Environment
from jinja2_s3loader import S3loader

dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses")
s3 = boto3.resource("s3")
table = dynamodb.Table("photo-booth-app")

def generate_template(imagePath):
    # Create an environment
    env = Environment(loader=S3loader('photobooth-assets', 'templates'))

    # Create the template
    template = env.get_template('email.html')

    return template.render(imagePath=imagePath)


def update_template(items):
    # Update template
    # (documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/update_template.html)
    reponse = ses_client.update_template(
        Template={
            "TemplateName": "photo_email_template",
            "SubjectPart": "Here's your photo booth picture!",
            "TextPart": "",
            "HtmlPart": generate_template(items['imagePath'])
        }
    )


def send_email(items):
    template_data = {
        'imagePath': items['imagePath']
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


def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={'requestId': request_id})
    items = response['Item']

    send_email(items)
