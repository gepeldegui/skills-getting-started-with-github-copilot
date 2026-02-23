"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_successful(client):
    """Test successful unregister from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    chess_club = response.json()["Chess Club"]
    
    assert "michael@mergington.edu" not in chess_club["participants"]
    assert len(chess_club["participants"]) == 1  # Was 2, now 1


def test_unregister_not_signed_up_returns_error(client):
    """Test that unregistering someone not signed up returns 400"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregister for non-existent activity returns 404"""
    response = client.delete(
        "/activities/Fake Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_unregister_then_signup_again(client):
    """Test that a student can unregister and then sign up again"""
    email = "michael@mergington.edu"
    
    # Unregister
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify they're back in the list
    response = client.get("/activities")
    chess_club = response.json()["Chess Club"]
    assert email in chess_club["participants"]


def test_unregister_multiple_students_from_same_activity(client):
    """Test unregistering multiple students from the same activity"""
    # Unregister both participants from Chess Club
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "daniel@mergington.edu"}
    )
    
    # Verify both were removed
    response = client.get("/activities")
    chess_club = response.json()["Chess Club"]
    assert len(chess_club["participants"]) == 0


def test_unregister_preserves_other_participants(client):
    """Test that unregistering one student doesn't affect others"""
    # Unregister one student
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    # Verify the other participant is still there
    response = client.get("/activities")
    chess_club = response.json()["Chess Club"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    assert "michael@mergington.edu" not in chess_club["participants"]
