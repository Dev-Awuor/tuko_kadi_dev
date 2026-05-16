"""Normalize Africa's Talking payloads into standard MessageEnvelopes."""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
import hashlib

class MessageEnvelope(BaseModel):
    """Standardized message format for the agent pipeline."""
    phone_hash: str
    session_id: str
    text: Optional[str] = ""
    channel: str  # "sms", "ussd", "whatsapp"
    media_url: Optional[str] = None
    raw_payload: dict

def _hash_phone(phone: str) -> str:
    """Hash phone number for zero-retention privacy."""
    # In production, use a salt from environment
    salt = "sauti-salt-2026" 
    return hashlib.sha256(f"{phone}{salt}".encode()).hexdigest()[:16]

def normalize_sms(payload: dict) -> MessageEnvelope:
    """Normalize AT SMS callback payload."""
    return MessageEnvelope(
        phone_hash=_hash_phone(payload.get("from", "unknown")),
        session_id=payload.get("id", "none"),
        text=payload.get("text", ""),
        channel="sms",
        raw_payload=payload
    )

def normalize_ussd(payload: dict) -> MessageEnvelope:
    """Normalize AT USSD callback payload."""
    return MessageEnvelope(
        phone_hash=_hash_phone(payload.get("phoneNumber", "unknown")),
        session_id=payload.get("sessionId", "none"),
        text=payload.get("text", ""),
        channel="ussd",
        raw_payload=payload
    )

def normalize_whatsapp(payload: dict) -> MessageEnvelope:
    """Normalize AT WhatsApp callback payload."""
    return MessageEnvelope(
        phone_hash=_hash_phone(payload.get("from", "unknown")),
        session_id=payload.get("id", f"wa-{payload.get('from')}"),
        text=payload.get("text", ""),
        channel="whatsapp",
        media_url=payload.get("mediaUrl"),
        raw_payload=payload
    )
