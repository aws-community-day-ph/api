import boto3

# Replace 'your-table-name' with the actual name of your DynamoDB table
table_name = 'photo-booth-app'

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Access the table
table = dynamodb.Table(table_name)

# Loop
response = table.scan()
items = response.get("Items", [])

ctr = 0

for i in items:
    try:
        if i['emails'] is None:
            print(i['requestId'])
    except Exception as e:
        print(f"exception: {e}")
    ctr += 1
    # for j in items:
    #     try:
    #         if i["emails"] == j["emails"] and i["requestId"] != j["requestId"]:
    #             print(f"{i} | {j}")
    #     except KeyError:
    #         print(i)

print(ctr)
