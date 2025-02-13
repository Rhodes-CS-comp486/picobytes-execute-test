import json
from imghdr import tests
from pathlib import Path
from fastapi.testclient import TestClient
from server_api import app

client = TestClient(app)
filepath = Path(__file__).parent / "testcode.json"
""
try:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
ccode = data.get("code", "")
tests = data.get("tests")

def test_api_submit_with_test():
    json_payload = {"code": ccode, "tests": tests}
    response = client.post("/submit", json=json_payload)
    assert response.status_code == 200


def test_api_submit_no_test():
    json_payload = {"code": ccode}
    response = client.post("/submit", json=json_payload)
    assert response.status_code == 200

def test_api_submit2_no_test():
    json_payload = {"code": ccode}
    response = client.post("/submit2", json=json_payload)
    assert response.status_code == 200
    json_response = response.json()
    assert "success" in json_response
    assert json_response["success"] is True

def test_api_submit2_with_test():
    json_payload = {"code": ccode, "tests": tests}
    response = client.post("/submit2", json=json_payload)
    assert response.status_code == 200
    json_response = response.json()
    assert "success" in json_response
    assert json_response["success"] is True
