from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert expected_activity in body
    assert "participants" in body[expected_activity]


def test_signup_for_activity_adds_email_to_participants():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@example.com"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_rejects_duplicate_email_for_same_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert email not in unregister_response.json()["participants"]


def test_unregister_missing_email_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
