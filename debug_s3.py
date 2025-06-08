import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
bucket_name = os.environ.get("SCW_BUCKET_NAME")
endpoint_url = os.environ.get("SCW_ENDPOINT_URL")
region = os.environ.get("SCW_REGION")
access_key = os.environ.get("SCW_ACCESS_KEY")
secret_key = os.environ.get("SCW_SECRET_KEY")

# --- Verification ---
print("--- S3 Debugger ---")
print(f"Attempting to connect with the following configuration:")
print(f"  Bucket Name: {bucket_name}")
print(f"  Endpoint URL: {endpoint_url}")
print(f"  Region: {region}")
print(f"  Access Key ID: {'SET' if access_key else 'NOT SET'}")
print("-" * 20)

# Basic validation
if not all([bucket_name, endpoint_url, region, access_key, secret_key]):
    print("\n❌ ERROR: One or more environment variables are missing in your .env file.")
    exit()

# --- S3 Client Initialization ---
try:
    s3_client = boto3.client(
        's3',
        endpoint_url=f"https://{endpoint_url}",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    print("✅ S3 client initialized successfully.")
    print(f"Listing all objects in bucket '{bucket_name}'...\n")

    # --- List All Objects ---
    # We are NOT using a prefix here to see everything.
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    contents = response.get('Contents', [])

    if not contents:
        print("➡️  Result: The list operation was successful, but the bucket is empty or no objects were returned.")
        print("   This could mean the bucket name or region is wrong, or the bucket is genuinely empty.")
    else:
        print(f"✅ Success! Found {len(contents)} object(s):")
        for i, obj in enumerate(contents):
            # This will print the exact key, which is the "full path" to the file.
            print(f"  {i+1}: Key = '{obj['Key']}'")

except ClientError as e:
    error_code = e.response.get("Error", {}).get("Code")
    print(f"\n❌ An S3 Client Error Occurred: {error_code}")
    print("   " + str(e))
    if error_code == "NoSuchBucket":
        print("\n   TROUBLESHOOTING: The bucket name in your .env file does not exist in the specified region.")
    elif error_code == "AccessDenied":
        print("\n   TROUBLESHOOTING: Your API key does not have permission to list objects in this bucket (s3:ListBucket).")
    elif error_code == "InvalidAccessKeyId":
         print("\n   TROUBLESHOOTING: The SCW_ACCESS_KEY is incorrect or invalid.")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")

print("\n--- Debugger Finished ---")