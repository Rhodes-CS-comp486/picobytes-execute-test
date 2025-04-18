import json

filepath1 = "./testcode.json"
filepath2 = "./encodedtest.json"

try:
    with open(filepath1, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ccode = data.get("code", "")
tests = data.get("tests")
timeout = data.get("timeout", 10)
pertesttimeout = data.get("perTestTimeout", 3)

json_payload = {"code": ccode, "tests": tests, "timeout": timeout, "perTestTimeout": pertesttimeout}

import requests
response = requests.post("http://127.0.0.1:5000/submit", json=json_payload)


print(response.json())



