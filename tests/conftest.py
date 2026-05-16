"""Global pytest configuration and mocks."""

import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture(autouse=True)
def mock_adk_runner(monkeypatch):
    """Mock the ADK Runner to avoid real API calls during unit tests."""
    mock_runner = MagicMock()
    
    # Mock run_async
    async def mock_run_async(*args, **kwargs):
        # Return a mock event with some text
        event = MagicMock()
        event.content.parts = [MagicMock(text="Mocked agent response")]
        yield event
        
    mock_runner.run_async = mock_run_async
    
    # Patch the runner in src.agents.runner
    monkeypatch.setattr("src.agents.runner._runner", mock_runner)
    return mock_runner

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set mock environment variables."""
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
    monkeypatch.setenv("AT_USERNAME", "sandbox")
    monkeypatch.setenv("AT_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

@pytest.fixture(autouse=True)
def mock_at_sdk(monkeypatch):
    """Mock Africa's Talking SDK."""
    mock_at = MagicMock()
    mock_at.SMS.send.return_value = {"status": "success"}
    monkeypatch.setattr("africastalking.initialize", MagicMock())
    monkeypatch.setattr("africastalking.SMS", mock_at.SMS)
