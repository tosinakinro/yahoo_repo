import os
from datetime import datetime
from flask import Flask
import boto3
import pytz
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["210 per 10 minutes"])
limiter.init_app(app)


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

@app.route('/')
@limiter.limit("210 per 10 minutes")
def display_latest_timestamp():
    try:
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='')['Contents']
        latest_object = max(objects, key=lambda obj: obj['LastModified'])

        obj = s3_client.get_object(Bucket=bucket_name, Key=latest_object['Key'])
        content = obj['Body'].read().decode('utf-8')
        return f"Most recent timestamp: {content}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    upload_timestamp()
    app.run(debug=True, host='0.0.0.0')  # Run the Flask app


