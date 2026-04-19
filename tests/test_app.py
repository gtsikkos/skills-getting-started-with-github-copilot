"""
Tests for the Mergington High School Activities API
"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test GET /activities returns all activities with correct structure"""
    # Arrange - no special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Should have activities

    # Check structure of first activity
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    email = "test_signup@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert f"{email} for {activity}" in result["message"]

    # Verify the participant was added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]


def test_signup_duplicate():
    """Test signing up for the same activity twice fails"""
    # Arrange
    email = "test_duplicate@mergington.edu"
    activity = "Programming Class"

    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act - attempt duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_invalid_activity():
    """Test signing up for non-existent activity fails"""
    # Arrange
    email = "test_invalid@mergington.edu"
    activity = "NonExistent Activity"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_unregister_success():
    """Test successful unregister from an activity"""
    # Arrange
    email = "test_unregister@mergington.edu"
    activity = "Gym Class"

    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert f"{email} from {activity}" in result["message"]

    # Verify the participant was removed
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]


def test_unregister_not_signed_up():
    """Test unregistering when not signed up fails"""
    # Arrange
    email = "test_not_signed@mergington.edu"
    activity = "Basketball Team"

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]


def test_unregister_invalid_activity():
    """Test unregistering from non-existent activity fails"""
    # Arrange
    email = "test_invalid_unregister@mergington.edu"
    activity = "Invalid Activity"

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]