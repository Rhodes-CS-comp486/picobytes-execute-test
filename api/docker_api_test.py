import requests

url = "http://127.0.0.1:8080/"
headers = {"Content-Type": "application/json"}
data = {"code": "xyz", "tests": "xyz"}

#response = requests.post(url, json=data, headers=headers)
response = requests.get(url)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
