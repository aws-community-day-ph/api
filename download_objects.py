import boto3
import os

# Replace 'your-bucket-name' with the name of the S3 bucket
bucket_name = 'photobooth-raw'

# Create an S3 client
s3 = boto3.client('s3')

# Get the current working directory of the Python script
current_directory = os.getcwd()

# Specify the folder name for downloads within the current directory
local_download_folder = os.path.join(current_directory, 'downloaded_files')

# Create the local download folder if it doesn't exist
os.makedirs(local_download_folder, exist_ok=True)

# Get a list of all objects (files) in the bucket
try:
    response = s3.list_objects_v2(Bucket=bucket_name)
    objects = response['Contents']

    # Download each object to the local folder
    for obj in objects:
        key = obj['Key']
        download_path = os.path.normpath(os.path.join(local_download_folder, key))
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        s3.download_file(bucket_name, key, download_path)
        print(f"Downloaded: {key}")

    print("All objects downloaded successfully.")

except Exception as e:
    print("Error:", e)
