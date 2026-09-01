from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert "student@example.com" not in response.json()["participants"]


def test_unregister_missing_email_returns_404():
    activity_name = "Chess Club"
    email = "missing@example.com"

    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 404
