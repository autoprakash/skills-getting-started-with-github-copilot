"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest


class TestSignupSuccess:
    """Test suite for successful signup operations."""

    def test_signup_new_student_success(self, client, mock_activities):
        """Arrange: Student not yet signed up.
        Act: POST signup request.
        Assert: Status 200, participant added."""
        # Arrange
        activity = "Chess Club"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in mock_activities[activity]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity}"

    def test_signup_empty_activity_gets_first_participant(self, client, mock_activities):
        """Arrange: Activity with no participants.
        Act: Signup student.
        Assert: Student becomes first participant."""
        # Arrange
        activity = "Drama Club"
        email = "bob@mergington.edu"
        initial_count = len(mock_activities[activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert len(mock_activities[activity]["participants"]) == initial_count + 1


class TestSignupDuplicate:
    """Test suite for duplicate signup prevention."""

    def test_duplicate_signup_rejected(self, client, mock_activities):
        """Arrange: Student already signed up.
        Act: Attempt POST signup with same email.
        Assert: Status 400, error message returned."""
        # Arrange
        activity = "Chess Club"
        email = mock_activities[activity]["participants"][0]  # "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_participant_count_unchanged_on_duplicate(self, client, mock_activities):
        """Arrange: Get initial participant count.
        Act: Try duplicate signup.
        Assert: Count unchanged."""
        # Arrange
        activity = "Chess Club"
        email = mock_activities[activity]["participants"][0]
        initial_count = len(mock_activities[activity]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert len(mock_activities[activity]["participants"]) == initial_count


class TestSignupErrors:
    """Test suite for signup error cases."""

    def test_signup_activity_not_found(self, client, mock_activities):
        """Arrange: Reference nonexistent activity.
        Act: POST signup for fake activity.
        Assert: Status 404."""
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_with_missing_email_param(self, client, mock_activities):
        """Arrange: No email parameter.
        Act: POST signup without email.
        Assert: FastAPI returns 422 Unprocessable Entity."""
        # Arrange
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup")

        # Assert
        assert response.status_code == 422  # FastAPI validation error
