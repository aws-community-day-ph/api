# src/handlers/send_emails.py
# initial testing by aki
# Use 971604 as requestId for testing


import boto3
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

dynamodb = boto3.resource("dynamodb")
client = boto3.client("ses")
table = dynamodb.Table("photo-booth-app")


def generate_template(name, imagePath):
    # Get path to template
    base_dir = Path(__file__).parent.parent
    templates_dir = base_dir / "assets" / "template"
    file_loader = FileSystemLoader(templates_dir)

    # Create an environment
    env = Environment(loader=file_loader)

    # Create the template
    template = env.get_template("email.html")

    return template.render(name=name, imagePath=imagePath)


def handler(event, context):
    # Extract request ID from path parameter
    request_id = event['pathParameters']['requestId']

    # Retrieve request data from DynamoDB based on request ID
    response = table.get_item(Key={'requestId': request_id})
    items = response['Item']

    for index, email in enumerate(items["emails"]):
        # Generate email body
        # to change: items[email] to items["names"][index]
        body = generate_template(email, items["imagePath"])

        # Generate email template
        # (documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/create_template.html)
        reponse = client.create_template(
            Template={
                "TemplateName": "AWS Photo Booth Email Template",
                "SubjectPart": "Here's your photo booth picture!",
                "TextPart": "",
                "HtmlPart": body
            }
        )

        # Send email
        client.send_templated_email(
            Source = 'anthony.basang18@gmail.com',
            Destination = {
                'ToAddresses': [email]
            },
            ReplyToAddresses = 'anthony.basang18@gmail.com',
            Template = 'AWS Photo Booth Email Template'
        )