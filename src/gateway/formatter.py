"""Format agent responses for specific Africa's Talking channels."""

import textwrap

def format_response(text: str, channel: str, end_session: bool = True) -> str:
    """Format text based on channel constraints."""
    
    if channel == "ussd":
        # USSD limit is 182 characters per screen
        # Prefix with CON (continue) or END (terminate)
        prefix = "END " if end_session else "CON "
        # Truncate and clean
        clean_text = text.replace("\n", " ").strip()
        truncated = textwrap.shorten(clean_text, width=178, placeholder="...")
        return f"{prefix}{truncated}"
    
    elif channel == "sms":
        # SMS standard is 160 chars, but AT handles multi-part.
        # We still keep it concise.
        return text.strip()
    
    elif channel == "whatsapp":
        # WhatsApp supports markdown and longer text.
        return text.strip()
    
    return text.strip()
