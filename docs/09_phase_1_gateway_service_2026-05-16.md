---
title: "Phase 1 — Project Scaffolding & Gateway Service"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Phase 1 — Project Scaffolding & Gateway Service

**Document ID:** SYM-IMPL-P1  
**Created:** 2026-05-16T10:12:00+03:00  
**Last Modified:** 2026-05-16T10:12:00+03:00  
**Phase Status:** ☐ Pending

---

## Phase Objective

Create the full project directory skeleton, implement the FastAPI gateway service with webhook endpoints for SMS/USSD/WhatsApp, build the input normalization and channel-aware output formatting pipeline, and verify the gateway accepts and responds to simulated Africa's Talking payloads.

---

## Dependencies & Blockers

| Dependency | Type | Resolution |
|-----------|------|-----------|
| Phase 0 complete | **BLOCKER** | All environment checks must pass |
| `.venv` active with dependencies installed | Required | `pip install -r requirements.txt` |
| `.env` file configured | Required | Copy from `.env.example` and fill values |

---

## Action Items

### Step 1.1 — Create Directory Structure

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:12 EAT]
```

```powershell
cd c:\Users\gvnrk\Documents\AG-HAL9000-IV\tuko_kadi_dev

# Create all directories
$dirs = @(
    "src", "src/agents", "src/tools", "src/guardrails", "src/gateway",
    "data", "tests", "scripts"
)
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
}

# Create __init__.py files for all Python packages
$inits = @(
    "src/__init__.py", "src/agents/__init__.py", "src/tools/__init__.py",
    "src/guardrails/__init__.py", "src/gateway/__init__.py"
)
foreach ($f in $inits) {
    New-Item -ItemType File -Path $f -Force | Out-Null
}
```

### Step 1.2 — Application Configuration Module

```
[Artifact Type: Source Code] | [File Name: src/config.py] | [Timestamp: 2026-05-16 10:13 EAT]
```

```python
"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings from environment."""

    # Google Cloud
    gcp_project: str = field(
        default_factory=lambda: os.environ["GOOGLE_CLOUD_PROJECT"]
    )
    gcp_location: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )

    # Africa's Talking
    at_username: str = field(
        default_factory=lambda: os.environ["AT_USERNAME"]
    )
    at_api_key: str = field(
        default_factory=lambda: os.environ["AT_API_KEY"]
    )
    at_environment: str = field(
        default_factory=lambda: os.getenv("AT_ENVIRONMENT", "sandbox")
    )

    # Vertex AI Search
    civic_datastore_id: str = field(
        default_factory=lambda: os.getenv("CIVIC_DATASTORE_ID", "")
    )

    # Application
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    max_session_timeout: int = field(
        default_factory=lambda: int(os.getenv("MAX_SESSION_TIMEOUT_SECONDS", "1800"))
    )
    port: int = field(
        default_factory=lambda: int(os.getenv("PORT", "8080"))
    )


def get_settings() -> Settings:
    """Factory that returns a singleton Settings instance."""
    return Settings()
```

### Step 1.3 — Message Envelope (Unified Input Model)

```
[Artifact Type: Source Code] | [File Name: src/gateway/normalizer.py] | [Timestamp: 2026-05-16 10:14 EAT]
```

```python
"""Normalize incoming webhook payloads from Africa's Talking
into a unified MessageEnvelope for the agent pipeline."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MessageEnvelope(BaseModel):
    """Unified message format across all communication channels.

    Every inbound message — whether from WhatsApp, SMS, or USSD —
    is normalized into this structure before entering the agent pipeline.
    """

    session_id: str = Field(
        ..., description="Unique session key: sha256(phone)[:16]:channel"
    )
    phone_hash: str = Field(
        ..., description="SHA-256 hash of the phone number (no raw PII)"
    )
    channel: str = Field(
        ..., description="Origin channel: 'whatsapp' | 'sms' | 'ussd'"
    )
    text: str = Field(
        default="", description="User message text"
    )
    media_url: str | None = Field(
        default=None, description="Attached media URL (WhatsApp images)"
    )
    ussd_session_id: str | None = Field(
        default=None, description="Africa's Talking USSD session ID"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def _hash_phone(phone: str) -> str:
    """One-way hash of phone number. Cannot be reversed."""
    normalized = phone.replace("+", "").replace(" ", "").replace("-", "")
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def normalize_sms(form_data: dict) -> MessageEnvelope:
    """Normalize an Africa's Talking SMS callback payload.

    AT SMS callback fields:
        from, to, text, date, id, linkId
    """
    phone = form_data.get("from", "")
    phone_hash = _hash_phone(phone)
    return MessageEnvelope(
        session_id=f"{phone_hash}:sms",
        phone_hash=phone_hash,
        channel="sms",
        text=form_data.get("text", "").strip(),
    )


def normalize_ussd(form_data: dict) -> MessageEnvelope:
    """Normalize an Africa's Talking USSD callback payload.

    AT USSD callback fields:
        sessionId, phoneNumber, networkCode, serviceCode, text
    """
    phone = form_data.get("phoneNumber", "")
    phone_hash = _hash_phone(phone)
    ussd_text = form_data.get("text", "")

    # USSD sends cumulative text separated by *.
    # Extract only the latest input segment.
    segments = ussd_text.split("*") if ussd_text else [""]
    latest_input = segments[-1].strip()

    return MessageEnvelope(
        session_id=f"{phone_hash}:ussd:{form_data.get('sessionId', '')}",
        phone_hash=phone_hash,
        channel="ussd",
        text=latest_input,
        ussd_session_id=form_data.get("sessionId"),
    )


def normalize_whatsapp(form_data: dict) -> MessageEnvelope:
    """Normalize an Africa's Talking WhatsApp callback payload.

    AT WhatsApp callback fields:
        from, text, mediaUrl, timestamp
    """
    phone = form_data.get("from", "")
    phone_hash = _hash_phone(phone)
    return MessageEnvelope(
        session_id=f"{phone_hash}:whatsapp",
        phone_hash=phone_hash,
        channel="whatsapp",
        text=form_data.get("text", "").strip(),
        media_url=form_data.get("mediaUrl"),
    )
```

### Step 1.4 — Channel-Aware Output Formatter

```
[Artifact Type: Source Code] | [File Name: src/gateway/formatter.py] | [Timestamp: 2026-05-16 10:15 EAT]
```

```python
"""Format agent responses for the target communication channel.

Each channel has strict constraints:
    - USSD: max 182 characters, CON/END prefix
    - SMS:  max 160 characters, plain text
    - WhatsApp: max 4096 characters, supports markdown
"""

from __future__ import annotations

USSD_MAX_CHARS = 182
SMS_MAX_CHARS = 160
WHATSAPP_MAX_CHARS = 4096


def format_response(text: str, channel: str, end_session: bool = False) -> str:
    """Format an agent response for the specified channel.

    Args:
        text: Raw agent response text.
        channel: Target channel ('ussd', 'sms', 'whatsapp').
        end_session: If True and channel is USSD, prefix with END instead of CON.

    Returns:
        Channel-formatted response string.
    """
    if channel == "ussd":
        return _format_ussd(text, end_session)
    elif channel == "sms":
        return _format_sms(text)
    elif channel == "whatsapp":
        return _format_whatsapp(text)
    else:
        return text


def _format_ussd(text: str, end_session: bool) -> str:
    """USSD: strict 182-char limit with CON/END prefix."""
    prefix = "END " if end_session else "CON "
    max_content = USSD_MAX_CHARS - len(prefix)
    content = text[:max_content]

    # If truncated, add ellipsis
    if len(text) > max_content:
        content = content[: max_content - 3] + "..."

    return f"{prefix}{content}"


def _format_sms(text: str) -> str:
    """SMS: 160-char limit, strip markdown formatting."""
    # Remove markdown bold/italic markers
    clean = text.replace("**", "").replace("__", "").replace("*", "").replace("_", "")
    # Remove markdown links [text](url) → text
    import re
    clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)

    if len(clean) > SMS_MAX_CHARS:
        clean = clean[: SMS_MAX_CHARS - 3] + "..."
    return clean


def _format_whatsapp(text: str) -> str:
    """WhatsApp: generous limit, keep markdown formatting."""
    if len(text) > WHATSAPP_MAX_CHARS:
        text = text[: WHATSAPP_MAX_CHARS - 3] + "..."
    return text
```

### Step 1.5 — Webhook Handlers

```
[Artifact Type: Source Code] | [File Name: src/gateway/webhooks.py] | [Timestamp: 2026-05-16 10:16 EAT]
```

```python
"""Africa's Talking webhook handlers.

Each handler:
1. Receives the AT POST callback
2. Normalizes the payload into a MessageEnvelope
3. Invokes the agent pipeline
4. Formats and returns the response for the channel
"""

from __future__ import annotations

import logging
from fastapi import APIRouter, Request, Response

from src.gateway.normalizer import (
    MessageEnvelope,
    normalize_sms,
    normalize_ussd,
    normalize_whatsapp,
)
from src.gateway.formatter import format_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhooks"])


async def _process_message(envelope: MessageEnvelope) -> str:
    """Send a normalized message through the agent pipeline.

    This is a placeholder that will be replaced in Phase 2
    when Msaidizi is wired up. For now, returns a stub response.
    """
    logger.info(
        "Processing message | session=%s channel=%s text=%s",
        envelope.session_id,
        envelope.channel,
        envelope.text[:50] if envelope.text else "(empty)",
    )
    # STUB: will be replaced with ADK runner invocation in Phase 2
    return (
        "Karibu! Welcome to Sauti ya Mwananchi. "
        "I can help you with: 1) Civic education 2) Polling stations "
        "3) Fact-checking 4) Election day guide. "
        "How can I help you today?"
    )


@router.post("/sms")
async def sms_webhook(request: Request):
    """Handle incoming SMS via Africa's Talking callback."""
    form_data = dict(await request.form())
    envelope = normalize_sms(form_data)

    agent_response = await _process_message(envelope)
    formatted = format_response(agent_response, "sms")

    logger.info("SMS response | session=%s len=%d", envelope.session_id, len(formatted))

    # AT SMS callbacks don't expect a response body for incoming.
    # We send the reply via AT SDK (Phase 8). For now, return 200.
    return {"status": "ok", "response": formatted}


@router.post("/ussd")
async def ussd_webhook(request: Request):
    """Handle USSD session via Africa's Talking callback.

    USSD requires a direct HTTP response body:
    - Prefix 'CON ' to keep session open
    - Prefix 'END ' to close session
    """
    form_data = dict(await request.form())
    envelope = normalize_ussd(form_data)

    is_initial = envelope.text == ""

    if is_initial:
        # First dial — show main menu
        response_text = (
            "Sauti ya Mwananchi\n"
            "1. Learn about your rights\n"
            "2. Find your polling station\n"
            "3. Check a claim\n"
            "4. Election day guide"
        )
        formatted = format_response(response_text, "ussd", end_session=False)
    else:
        agent_response = await _process_message(envelope)
        formatted = format_response(agent_response, "ussd", end_session=False)

    return Response(content=formatted, media_type="text/plain")


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """Handle incoming WhatsApp message via Africa's Talking callback."""
    form_data = dict(await request.form())
    envelope = normalize_whatsapp(form_data)

    agent_response = await _process_message(envelope)
    formatted = format_response(agent_response, "whatsapp")

    logger.info(
        "WhatsApp response | session=%s len=%d", envelope.session_id, len(formatted)
    )
    return {"status": "ok", "response": formatted}
```

### Step 1.6 — FastAPI Main Application

```
[Artifact Type: Source Code] | [File Name: src/main.py] | [Timestamp: 2026-05-16 10:17 EAT]
```

```python
"""Sauti ya Mwananchi — FastAPI Gateway Entrypoint.

This is the main application that:
1. Receives webhook callbacks from Africa's Talking (SMS, USSD, WhatsApp)
2. Normalizes inputs into a unified MessageEnvelope
3. Routes through the multi-agent pipeline (ADK)
4. Returns channel-formatted responses
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.gateway.webhooks import router as webhook_router
from src.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Sauti ya Mwananchi starting | project=%s", settings.gcp_project)
    yield
    logger.info("Sauti ya Mwananchi shutting down")


app = FastAPI(
    title="Sauti ya Mwananchi",
    description="AI-powered civic participation platform for Kenyan voters",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register webhook routes
app.include_router(webhook_router)


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "service": "sauti-ya-mwananchi",
        "version": "0.1.0",
    }


@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "Sauti ya Mwananchi",
        "description": "AI-powered civic participation platform",
        "endpoints": {
            "health": "/health",
            "sms_webhook": "/webhook/sms",
            "ussd_webhook": "/webhook/ussd",
            "whatsapp_webhook": "/webhook/whatsapp",
        },
    }
```

### Step 1.7 — Gateway Integration Tests

```
[Artifact Type: Test Suite] | [File Name: tests/test_webhooks.py] | [Timestamp: 2026-05-16 10:18 EAT]
```

```python
"""Tests for webhook handlers and message normalization."""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.gateway.normalizer import normalize_sms, normalize_ussd, normalize_whatsapp
from src.gateway.formatter import format_response


client = TestClient(app)


# ── Health & Root ──────────────────────────────────────────────

class TestHealthEndpoints:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Sauti ya Mwananchi" in response.json()["service"]


# ── Normalizer ─────────────────────────────────────────────────

class TestNormalizer:
    def test_sms_normalization(self):
        payload = {"from": "+254700000000", "to": "12345", "text": "What are my rights?"}
        envelope = normalize_sms(payload)
        assert envelope.channel == "sms"
        assert envelope.text == "What are my rights?"
        assert "+254" not in envelope.session_id  # Phone is hashed
        assert "+254" not in envelope.phone_hash

    def test_ussd_normalization_initial(self):
        payload = {
            "sessionId": "sess123",
            "phoneNumber": "+254700000000",
            "serviceCode": "*384*123#",
            "text": "",
        }
        envelope = normalize_ussd(payload)
        assert envelope.channel == "ussd"
        assert envelope.text == ""
        assert envelope.ussd_session_id == "sess123"

    def test_ussd_normalization_with_input(self):
        payload = {
            "sessionId": "sess123",
            "phoneNumber": "+254700000000",
            "serviceCode": "*384*123#",
            "text": "1*2",
        }
        envelope = normalize_ussd(payload)
        assert envelope.text == "2"  # Latest segment only

    def test_whatsapp_normalization(self):
        payload = {"from": "+254700000000", "text": "Hello", "mediaUrl": "https://example.com/img.jpg"}
        envelope = normalize_whatsapp(payload)
        assert envelope.channel == "whatsapp"
        assert envelope.media_url == "https://example.com/img.jpg"

    def test_phone_hash_consistency(self):
        p1 = normalize_sms({"from": "+254700000000", "text": ""})
        p2 = normalize_sms({"from": "+254700000000", "text": ""})
        assert p1.phone_hash == p2.phone_hash

    def test_phone_hash_strips_formatting(self):
        p1 = normalize_sms({"from": "+254 700 000 000", "text": ""})
        p2 = normalize_sms({"from": "254700000000", "text": ""})
        assert p1.phone_hash == p2.phone_hash


# ── Formatter ──────────────────────────────────────────────────

class TestFormatter:
    def test_ussd_con_prefix(self):
        result = format_response("Hello", "ussd", end_session=False)
        assert result.startswith("CON ")

    def test_ussd_end_prefix(self):
        result = format_response("Goodbye", "ussd", end_session=True)
        assert result.startswith("END ")

    def test_ussd_truncation(self):
        long_text = "A" * 300
        result = format_response(long_text, "ussd")
        assert len(result) <= 182

    def test_sms_truncation(self):
        long_text = "B" * 300
        result = format_response(long_text, "sms")
        assert len(result) <= 160

    def test_sms_strips_markdown(self):
        result = format_response("**bold** and *italic*", "sms")
        assert "**" not in result
        assert "*" not in result

    def test_whatsapp_preserves_markdown(self):
        result = format_response("**bold** text", "whatsapp")
        assert "**bold**" in result


# ── Webhook Endpoints ──────────────────────────────────────────

class TestWebhookEndpoints:
    def test_sms_webhook(self):
        response = client.post(
            "/webhook/sms",
            data={"from": "+254700000000", "to": "12345", "text": "Hello"},
        )
        assert response.status_code == 200
        assert "response" in response.json()

    def test_ussd_webhook_initial(self):
        response = client.post(
            "/webhook/ussd",
            data={
                "sessionId": "test-session",
                "phoneNumber": "+254700000000",
                "serviceCode": "*384*123#",
                "text": "",
            },
        )
        assert response.status_code == 200
        body = response.text
        assert body.startswith("CON ")
        assert "Sauti ya Mwananchi" in body

    def test_ussd_webhook_with_selection(self):
        response = client.post(
            "/webhook/ussd",
            data={
                "sessionId": "test-session",
                "phoneNumber": "+254700000000",
                "serviceCode": "*384*123#",
                "text": "1",
            },
        )
        assert response.status_code == 200
        body = response.text
        assert body.startswith("CON ") or body.startswith("END ")

    def test_whatsapp_webhook(self):
        response = client.post(
            "/webhook/whatsapp",
            data={"from": "+254700000000", "text": "Help me"},
        )
        assert response.status_code == 200
```

### Step 1.8 — Verify Phase 1

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:19 EAT]
```

```powershell
# 1. Run the test suite
pytest tests/test_webhooks.py -v

# 2. Start the server
uvicorn src.main:app --reload --port 8080

# 3. (In a separate terminal) Test endpoints with curl
# Health
curl http://localhost:8080/health

# SMS webhook
curl -X POST http://localhost:8080/webhook/sms -d "from=+254700000000&to=12345&text=Hello"

# USSD initial dial
curl -X POST http://localhost:8080/webhook/ussd -d "sessionId=s1&phoneNumber=+254700000000&serviceCode=*384*123#&text="

# USSD with selection
curl -X POST http://localhost:8080/webhook/ussd -d "sessionId=s1&phoneNumber=+254700000000&serviceCode=*384*123#&text=1"
```

---

## Required Artifacts — Summary

| # | Artifact Type | File Name | Description |
|---|--------------|-----------|-------------|
| 1 | Source Code | `src/config.py` | Settings from environment variables |
| 2 | Source Code | `src/gateway/normalizer.py` | MessageEnvelope model + AT payload normalizers |
| 3 | Source Code | `src/gateway/formatter.py` | Channel-aware response formatting (USSD/SMS/WhatsApp) |
| 4 | Source Code | `src/gateway/webhooks.py` | FastAPI webhook route handlers |
| 5 | Source Code | `src/main.py` | FastAPI application entrypoint |
| 6 | Test Suite | `tests/test_webhooks.py` | 14 tests for normalizer, formatter, and webhook endpoints |

---

## Exit Criteria

Phase 1 is complete when ALL of the following are true:

- [ ] All `__init__.py` files exist in `src/`, `src/agents/`, `src/tools/`, `src/guardrails/`, `src/gateway/`
- [ ] `src/config.py` loads settings from `.env` without error
- [ ] `src/gateway/normalizer.py` correctly normalizes SMS, USSD, and WhatsApp payloads
- [ ] `src/gateway/formatter.py` enforces channel character limits (USSD ≤ 182, SMS ≤ 160)
- [ ] `src/gateway/webhooks.py` exposes `/webhook/sms`, `/webhook/ussd`, `/webhook/whatsapp`
- [ ] `src/main.py` starts without error on port 8080
- [ ] `/health` returns `{"status": "healthy"}`
- [ ] USSD initial dial returns `CON Sauti ya Mwananchi...` with menu
- [ ] `pytest tests/test_webhooks.py -v` — all 14 tests pass
- [ ] Phone numbers are NEVER present in session IDs (only hashes)
