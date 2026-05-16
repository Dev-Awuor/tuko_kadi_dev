"""Tests for Gateway Webhooks."""

from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_sms_webhook():
    payload = {
        "from": "+254712345678",
        "to": "12345",
        "text": "Hello Sauti",
        "id": "sms-123"
    }
    response = client.post("/webhook/sms", data=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_ussd_initial_dial():
    payload = {
        "sessionId": "ussd-123",
        "phoneNumber": "+254712345678",
        "serviceCode": "*384*123#",
        "text": ""
    }
    response = client.post("/webhook/ussd", data=payload)
    assert response.status_code == 200
    assert response.text.startswith("CON")
    assert "Welcome" in response.text

def test_ussd_selection():
    payload = {
        "sessionId": "ussd-123",
        "phoneNumber": "+254712345678",
        "serviceCode": "*384*123#",
        "text": "1"
    }
    response = client.post("/webhook/ussd", data=payload)
    assert response.status_code == 200
    assert response.text.startswith("END")
    assert "mocked" in response.text.lower()
