"""Tests for the GET /activities endpoint"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have 9 activities
    assert len(activities) == 9
    
    # Check that specific activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        # Each activity should have these required fields
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Data types should be correct
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that participants are email strings"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Should be an email format


def test_chess_club_has_initial_participants(client):
    """Test that Chess Club has the expected participants"""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
