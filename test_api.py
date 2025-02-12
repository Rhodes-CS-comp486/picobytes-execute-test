from fastapi.testclient import TestClient
from server_api import app


client = TestClient(app)