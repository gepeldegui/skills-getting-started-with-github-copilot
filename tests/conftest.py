import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
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
            "description": "Competitive basketball team for interscholastic games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and play friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["ava@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and improve acting skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions",
            "schedule": "Mondays and Thursdays, 3:45 PM - 5:15 PM",
            "max_participants": 16,
            "participants": ["amelia@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["chloe@mergington.edu"]
        }
    }
    
    yield
    
    # Reset to original state after test
    activities.clear()
    for activity_name, activity_data in original_activities.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
