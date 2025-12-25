import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Original activities data for reset
original_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
    "description": "Learn programming fundamentals and build software projects",
    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
    "max_participants": 20,
    "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
    "description": "Physical education and sports activities",
    "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
    "max_participants": 30,
    "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
    "description": "Competitive basketball league and practice",
    "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
    "max_participants": 15,
    "participants": ["james@mergington.edu"]
    },
    "Soccer Club": {
    "description": "Recreational and competitive soccer",
    "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
    "max_participants": 20,
    "participants": ["lucas@mergington.edu"]
    },
    "Debate Team": {
    "description": "Develop public speaking and critical thinking skills",
    "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
    "max_participants": 18,
    "participants": ["isabella@mergington.edu", "alexander@mergington.edu"]
    },
    "Science Club": {
    "description": "Explore scientific concepts through experiments and projects",
    "schedule": "Thursdays, 4:00 PM - 5:30 PM",
    "max_participants": 25,
    "participants": ["noah@mergington.edu"]
    },
    "Art Studio": {
    "description": "Painting, drawing, and sculpture",
    "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
    "max_participants": 16,
    "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Drama Club": {
    "description": "Theater performances and acting workshops",
    "schedule": "Fridays, 4:00 PM - 6:00 PM",
    "max_participants": 20,
    "participants": ["amelia@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the activities to original state before each test
    from src.app import activities
    activities.clear()
    activities.update(original_activities.copy())

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    # Test signing up for an activity
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Check that the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]