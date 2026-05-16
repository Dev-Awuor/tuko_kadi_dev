"""Africa's Talking SDK integration for outbound replies."""

import africastalking
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)

def send_sms(to_phone: str, message: str):
    """Send an outbound SMS reply."""
    settings = get_settings()
    africastalking.initialize(
        username=settings.at_username,
        api_key=settings.at_api_key
    )
    sms = africastalking.SMS
    try:
        response = sms.send(message, [to_phone])
        logger.info(f"SMS sent to {to_phone}: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        return None

def send_whatsapp(to_phone: str, message: str):
    """Send an outbound WhatsApp reply."""
    # Note: AT WhatsApp API often shares the same SMS endpoint or requires a channel ID.
    # For the hackathon, we focus on SMS/USSD, but keep the stub.
    logger.info(f"WhatsApp (stub) to {to_phone}: {message}")
    return send_sms(to_phone, message)
