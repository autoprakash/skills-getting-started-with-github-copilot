"""Tests for DELETE /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest


class TestUnregisterSuccess:
    """Test suite for successful unregister operations."""

    def test_unregister_signed_up_student_success(self, client, mock_activities):
        """Arrange: Student is signed up.
        Act: DELETE unregister.
        Assert: Status 200, participant removed."""
        # Arrange
        activity = "Chess Club"
        email = mock_activities[activity]["participants"][0]  # "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email not in mock_activities[activity]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity}"

    def test_participant_count_decreases(self, client, mock_activities):
        """Arrange: Get initial count from activity with participants.
        Act: Unregister a participant.
        Assert: Count decreases by 1."""
        # Arrange
        activity = "Chess Club"
        email = mock_activities[activity]["participants"][0]
        initial_count = len(mock_activities[activity]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert len(mock_activities[activity]["participants"]) == initial_count - 1


class TestUnregisterErrors:
    """Test suite for unregister error cases."""

    def test_unregister_not_signed_up(self, client, mock_activities):
        """Arrange: Student not in participants list.
        Act: Attempt DELETE unregister.
        Assert: Status 400, error message."""
        # Arrange
        activity = "Chess Club"
        email = "nobody@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_from_empty_activity(self, client, mock_activities):
        """Arrange: Activity with no participants.
        Act: Try to unregister from it.
        Assert: Status 400."""
        # Arrange
        activity = "Drama Club"  # Has no participants
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400

    def test_unregister_activity_not_found(self, client, mock_activities):
        """Arrange: Reference nonexistent activity.
        Act: DELETE from fake activity.
        Assert: Status 404."""
        # Arrange
        fake_activity = "Fake Club"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_with_missing_email_param(self, client, mock_activities):
        """Arrange: No email parameter.
        Act: DELETE unregister without email.
        Assert: Status 422 Unprocessable Entity."""
        # Arrange
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/signup")

        # Assert
        assert response.status_code == 422
