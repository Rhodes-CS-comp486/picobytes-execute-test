import json
from imghdr import tests
from pathlib import Path
from fastapi.testclient import TestClient
from server_api import app

client = TestClient(app)
filepath1 = Path(__file__).parent / "testcode.json"
filepath2 = Path(__file__).parent / "encodedtest.json"

try:
    with open(filepath1, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ccode = data.get("code", "")
tests = data.get("tests")

try:
    with open(filepath2, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ecode = data.get("code", "")
etests = data.get("tests")

def test_api_submit_with_test():
    json_payload = {"code": ccode, "tests": tests}
    response = client.post("/submit", json=json_payload)
    assert response.status_code == 200


def test_api_submit_no_test():
    json_payload = {"code": ccode}
    response = client.post("/submit", json=json_payload)
    assert response.status_code == 200

def test_encoded_json_with_test():
    json_payload = {"code": ecode, "tests": etests}
    response = client.post("/encoded", json=json_payload)
    assert response.status_code == 200

def test_encoded_json_no_test():
    json_payload = {"code": ecode}
    response = client.post("/encoded", json=json_payload)
    assert response.status_code == 200
