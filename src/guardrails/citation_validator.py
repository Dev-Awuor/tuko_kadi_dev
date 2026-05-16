"""Enforce citations in agent responses."""

import re

CITATION_PATTERN = re.compile(r'\[Source:\s*[^\]]+\]', re.I)

def validate_citations(response: str) -> str:
    """Ensure responses have sources if they make civic claims."""
    # This is a simple heuristic: if it looks like a factual claim, check for source
    if any(keyword in response.lower() for keyword in ["article", "section", "act", "constitution"]):
        if not CITATION_PATTERN.search(response):
            return response + "\n\n[Note: Please verify this with official IEBC documents.]"
    return response
