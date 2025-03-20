import json

filepath1 = "./infinite.json"
filepath2 = "./encodedtest.json"

try:
    with open(filepath1, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ccode = data.get("code", "")
tests = data.get("tests")

json_payload = {"code": ccode, "tests": tests}

import requests
response = requests.post("http://127.0.0.1:5001/submit", json=json_payload)


print(response.json())



