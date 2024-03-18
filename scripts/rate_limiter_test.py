import requests

# Update with the URL of your Flask application
url = 'http://localhost:5000/'

# Number of requests to send
request_count = 220

for i in range(request_count):
    response = requests.get(url)
    print(f"Request {i+1}: Status code {response.status_code}")