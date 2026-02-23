"""Tests for the POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_successful(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity"""
    # First signup
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    
    assert "newstudent@mergington.edu" in chess_club["participants"]
    assert len(chess_club["participants"]) == 3  # 2 original + 1 new


def test_signup_duplicate_email_returns_error(client):
    """Test that signing up with duplicate email returns 400 error"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}  # Already signed up
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Fake Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_signup_multiple_students(client):
    """Test that multiple students can sign up for the same activity"""
    student1 = "student1@mergington.edu"
    student2 = "student2@mergington.edu"
    
    response1 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": student1}
    )
    response2 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": student2}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both were added
    response = client.get("/activities")
    tennis_club = response.json()["Tennis Club"]
    assert student1 in tennis_club["participants"]
    assert student2 in tennis_club["participants"]


def test_signup_various_activities(client):
    """Test that students can sign up for different activities"""
    email = "versatile@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify student is in all activities
    response = client.get("/activities")
    all_activities = response.json()
    for activity in activities:
        assert email in all_activities[activity]["participants"]
