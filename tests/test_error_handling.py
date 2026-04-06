"""Tests for edge cases and error handling using AAA pattern."""

import pytest


class TestParameterValidation:
    """Test suite for request parameter validation."""

    def test_signup_invalid_email_format_not_enforced(self, client, mock_activities):
        """Arrange: Invalid email format (no validation in current API).
        Act: Signup with invalid email.
        Assert: Still succeeds (no email format validation implemented)."""
        # Arrange
        activity = "Chess Club"
        invalid_email = "notanemail"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": invalid_email}
        )

        # Assert
        # Current API doesn't validate email format
        assert response.status_code == 200
        assert invalid_email in mock_activities[activity]["participants"]


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_activity_name_with_special_characters(self, client, mock_activities):
        """Arrange: Activity name with spaces/special chars.
        Act: POST signup for activity with encoded name.
        Assert: Proper 404 if not found."""
        # Arrange
        fake_activity = "Fake & Activity"
        email = "test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_email_with_special_characters(self, client, mock_activities):
        """Arrange: Email with special characters (URL encoded).
        Act: Signup with complex email.
        Assert: Successfully added (current API accepts any string)."""
        # Arrange
        activity = "Chess Club"
        email = "john+test@example.com"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in mock_activities[activity]["participants"]

    def test_consecutive_signup_and_unregister(self, client, mock_activities):
        """Arrange: Student not signed up.
        Act: Signup, then immediately unregister.
        Assert: Both operations succeed, student not in final list."""
        # Arrange
        activity = "Drama Club"
        email = "test@mergington.edu"

        # Act - Signup
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200
        assert email not in mock_activities[activity]["participants"]

    def test_multiple_signup_and_unregister_sequence(self, client, mock_activities):
        """Arrange: Multiple students not yet signed up.
        Act: Sign up multiple students, unregister one, verify others remain.
        Assert: Only specified student is removed."""
        # Arrange
        activity = "Drama Club"
        email1 = "alice@mergington.edu"
        email2 = "bob@mergington.edu"

        # Act - Sign up first student
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email1}
        )

        # Act - Sign up second student
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email2}
        )

        # Act - Unregister first student
        unregister_response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email1}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert unregister_response.status_code == 200
        assert email1 not in mock_activities[activity]["participants"]
        assert email2 in mock_activities[activity]["participants"]
