"""Prompt injection detection."""

import re

INJECTION_PATTERNS = [
    re.compile(r'ignore\s+(all\s+)?(previous|prior)\s+instructions', re.I),
    re.compile(r'you\s+are\s+now\s+a\s+political', re.I),
    re.compile(r'pretend\s+to\s+be', re.I),
    re.compile(r'bypass\s+safety', re.I),
    re.compile(r'forget\s+all\s+rules', re.I)
]

def detect_injection(text: str) -> bool:
    """Check for prompt injection attempts."""
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            return True
    return False

INJECTION_REFUSAL = (
    "I am designed to provide factual civic education only. "
    "I cannot change my role or override my guidelines."
)
