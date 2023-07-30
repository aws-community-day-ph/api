import requests
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("photo-booth-app")

items = table.scan().get("Items")

for item in items:  # item.keys() = ["imagePath", "emails", "requestId", "status"]
    # First check if request id is in proper format `item["requestId"][:-3] == R-20230729-`
    if item["requestId"][:-3] != "R-20230729-":
        continue

    # Check if imagePath exists (meaning, it's a valid and verified request)
    if item["status"] != "uploaded":
        continue

    requestId = item["requestId"]
    endpoint = f"https://z3efpmw3k2.execute-api.ap-southeast-1.amazonaws.com/dev/requests/{requestId}"

    response = requests.get(endpoint)

    if response.status_code != 200:
        print(f"{requestId}: {response.status_code}")
        continue

    print(f"{requestId}: {response.json()}")


# requestId = "971604"
# api_endpoint = f"https://z3efpmw3k2.execute-api.ap-southeast-1.amazonaws.com/dev/send_ses/{requestId}"

# response = requests.post(api_endpoint)

# print(response.json())