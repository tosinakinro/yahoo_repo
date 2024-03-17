#!/usr/bin/env python3
import boto3
from datetime import datetime
import os
import pytz

s3_client = boto3.client('s3')
kms_key_id = os.getenv('KMS_KEY_ID')
bucket_name = os.getenv('BUCKET_NAME')

def upload_timestamp():
    s3_client = boto3.client('s3')
    cst_timezone = pytz.timezone('America/Chicago')
    timestamp = datetime.now(cst_timezone).isoformat()

    message_content = f"Hi Yahoo team! This file was created at {timestamp}"

    file_name = f"{timestamp}.txt"
    s3_client.put_object(
        Body=message_content,
        Bucket=bucket_name,
        Key=file_name,
        ServerSideEncryption='aws:kms',
        SSEKMSKeyId=kms_key_id)

    print(f"Uploaded {file_name} to {bucket_name}")

if __name__ == '__main__':
    upload_timestamp()



