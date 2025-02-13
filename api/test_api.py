from fastapi.testclient import TestClient
from server_api import app
from pathlib import Path

directory = Path("")
filepath = directory / "testcode.txt"
print(filepath)
with open(filepath, "r" ) as f:
    ccode = f.read()
client = TestClient(app)

def test_api_submit_no_test():
    response = client.post("/submit", json={"code": ccode})
    assert response.status_code == 200
def test_api_submit_with_test():
    response = client.post("/submit", json={"code": ccode, "tests": "this is a test"})
    assert response.status_code == 200
