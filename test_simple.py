#!/usr/bin/env python
import sys
sys.path.insert(0, '/workspaces/skills-getting-started-with-github-copilot/src')

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    print("test_get_activities passed")

def test_signup():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    print("test_signup passed")

if __name__ == "__main__":
    test_get_activities()
    test_signup()
    print("All tests passed!")