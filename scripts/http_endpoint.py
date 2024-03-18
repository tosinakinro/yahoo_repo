import os
import boto3
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["210 per 10 minutes"])
limiter.init_app(app)


s3_client = boto3.client('s3')
bucket_name = 'my-unique-yahoo-bucket-name-4klma1zs'


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
    app.run(debug=True, host='0.0.0.0')  # Run the Flask app