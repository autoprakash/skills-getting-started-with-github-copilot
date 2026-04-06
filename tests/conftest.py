"""Shared fixtures for API tests using AAA pattern."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Arrange: Provide a TestClient for API testing.
    
    This fixture creates a test client that can make requests
    to the FastAPI application without running a server.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Arrange: Provide isolated test data for each test.
    
    Returns a fresh copy of test activities that won't be
    modified across test runs due to isolation via monkeypatch.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["emma@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act in plays and improve theatrical skills",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": []
        }
    }


@pytest.fixture
def mock_activities(monkeypatch, sample_activities):
    """Arrange: Replace app's global activities dict with test data.
    
    Uses monkeypatch to isolate tests by replacing the global
    activities dictionary with fresh test data for each test.
    This prevents test interference.
    """
    import src.app as app_module
    monkeypatch.setattr(app_module, "activities", sample_activities)
    return sample_activities
