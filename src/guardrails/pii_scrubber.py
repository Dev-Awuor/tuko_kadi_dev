"""PII detection and removal."""

import re
import logging

logger = logging.getLogger(__name__)

# Patterns for Kenyan National ID (7-8 digits) and Phone Numbers
ID_PATTERN = re.compile(r'\b\d{7,8}\b')
PHONE_PATTERN = re.compile(r'(\+?254|0[17])\d{8,9}\b')

def scrub_pii(text: str) -> tuple[str, list[str]]:
    """Remove PII from text."""
    found = []
    
    if PHONE_PATTERN.search(text):
        text = PHONE_PATTERN.sub("[REDACTED_PHONE]", text)
        found.append("phone")
        
    if ID_PATTERN.search(text):
        # Avoid redacting years (2022-2027)
        matches = ID_PATTERN.findall(text)
        for m in matches:
            if not (2000 <= int(m) <= 2030):
                text = text.replace(m, "[REDACTED_ID]")
                found.append("id")
                
    return text, found
