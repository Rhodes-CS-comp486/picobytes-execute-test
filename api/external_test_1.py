import json

filepath1 = "./testcode1.json"
filepath2 = "./encodedtest.json"

try:
    with open(filepath2, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ccode = data.get("code", "")
tests = data.get("tests")

json_payload = {"code": ccode, "tests": tests}

import requests
response = requests.post("http://10.20.42.23:5000/encoded", json=json_payload)


print(response.json())



