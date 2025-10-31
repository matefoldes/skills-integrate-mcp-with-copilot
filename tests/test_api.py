"""Tests for API endpoints."""

from fastapi import status


def test_get_activities(client):
    """Test GET /activities endpoint."""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

    # Check structure of returned data
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.com"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Signed up student@example.com for Chess Club" in response.json()["message"]

    # Verify the student is now in the participants list
    response = client.get("/activities")
    data = response.json()
    assert "student@example.com" in data["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signup for an activity that doesn't exist."""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@example.com"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email(client):
    """Test that a student cannot sign up twice for the same activity."""
    email = "duplicate@example.com"

    # First signup - should succeed
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert response.status_code == status.HTTP_200_OK

    # Second signup - should fail
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full(client):
    """Test that signup fails when activity is at capacity."""
    # Sign up max number of students
    for i in range(12):  # Chess Club has max 12 participants
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": f"student{i}@example.com"},
        )
        assert response.status_code == status.HTTP_200_OK

    # Try to sign up one more student
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student13@example.com"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "full" in response.json()["detail"].lower()


def test_unregister_from_activity_success(client):
    """Test successful unregister from an activity."""
    email = "unregister@example.com"

    # First, sign up
    client.post(
        "/activities/Programming Class/signup",
        params={"email": email},
    )

    # Then unregister
    response = client.delete(
        "/activities/Programming Class/unregister",
        params={"email": email},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Unregistered" in response.json()["message"]

    # Verify the student is no longer in the participants list
    response = client.get("/activities")
    data = response.json()
    assert email not in data["Programming Class"]["participants"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregister from an activity that doesn't exist."""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@example.com"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_signed_up(client):
    """Test unregister when student is not signed up for the activity."""
    response = client.delete(
        "/activities/Gym Class/unregister",
        params={"email": "notsignedup@example.com"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not signed up" in response.json()["detail"]


def test_root_redirects_to_static(client):
    """Test that root path redirects to static index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "/static/index.html"


def test_multiple_students_can_signup(client):
    """Test that multiple students can sign up for the same activity."""
    emails = ["student1@example.com", "student2@example.com", "student3@example.com"]

    for email in emails:
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email},
        )
        assert response.status_code == status.HTTP_200_OK

    # Verify all students are in the participants list
    response = client.get("/activities")
    data = response.json()
    participants = data["Programming Class"]["participants"]
    for email in emails:
        assert email in participants


def test_student_can_signup_for_multiple_activities(client):
    """Test that a student can sign up for multiple different activities."""
    email = "multisport@example.com"

    # Sign up for multiple activities
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert response1.status_code == status.HTTP_200_OK

    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email},
    )
    assert response2.status_code == status.HTTP_200_OK

    # Verify student is in both activities
    response = client.get("/activities")
    data = response.json()
    assert email in data["Chess Club"]["participants"]
    assert email in data["Programming Class"]["participants"]
