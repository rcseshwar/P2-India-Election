"""
Tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client, mocking external dependencies."""
    # Import with mocking to avoid requiring GCP credentials in tests
    from unittest.mock import patch, MagicMock

    with patch("services.firestore_service.firestore_service") as mock_fs:
        mock_fs.create_session = MagicMock()
        mock_fs.save_message = MagicMock()
        mock_fs.get_chat_history = MagicMock(return_value=[])
        mock_fs.save_feedback = MagicMock()

        from main import app
        with TestClient(app) as c:
            yield c


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "project_id" in data


class TestAgentsEndpoint:
    """Tests for /api/agents endpoint."""

    def test_list_agents(self, client):
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 6

    def test_agent_structure(self, client):
        response = client.get("/api/agents")
        agents = response.json()["agents"]
        for agent in agents:
            assert "name" in agent
            assert "title" in agent
            assert "icon" in agent
            assert "description" in agent
            assert "topics" in agent


class TestSessionEndpoint:
    """Tests for /api/session endpoint."""

    def test_create_session(self, client):
        response = client.post("/api/session?user_id=test-user")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["created"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
