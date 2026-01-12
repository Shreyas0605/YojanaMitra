import requests
import json

url = 'http://localhost:5000/api/admin/login'
headers = {'Content-Type': 'application/json'}
data = {
    'email': 'admin@yojanamitra.gov.in',
    'password': 'admin123'
}

print(f"Testing Login API: {url}")
try:
    response = requests.post(url, headers=headers, json=data, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
