"""Tests for basic API endpoints (GET / and GET /activities) using AAA pattern."""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_all_activities_success(self, client, mock_activities):
        """Arrange: No setup needed beyond fixture.
        Act: Send GET request to /activities.
        Assert: Verify status 200 and all activities returned."""
        # Arrange
        expected_count = 3

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Drama Club" in activities

    def test_get_activities_returns_correct_structure(self, client, mock_activities):
        """Arrange: Mock activities fixture.
        Act: Fetch activities.
        Assert: Verify each activity has required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_with_participants(self, client, mock_activities):
        """Arrange: Mock activities with participants.
        Act: Get activities.
        Assert: Verify participants list is accurate."""
        # Arrange
        # (activities already have participants from sample_activities fixture)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
        assert activities["Drama Club"]["participants"] == []


class TestRootRedirect:
    """Test suite for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Arrange: No setup needed.
        Act: Send GET to root.
        Assert: Verify redirect to /static/index.html."""
        # Arrange
        # (no setup)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]

    def test_root_redirect_follows(self, client):
        """Arrange: No setup.
        Act: Follow redirects from root.
        Assert: Verify final response is 200."""
        # Arrange
        # (no setup)

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
