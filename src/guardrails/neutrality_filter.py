"""Political neutrality post-filter."""

import re

BIAS_PATTERNS = [
    re.compile(r'(you\s+should|recommend\s+(you\s+)?)vote\s+for', re.I),
    re.compile(r'the\s+best\s+candidate\s+is', re.I),
    re.compile(r'I\s+recommend\s+voting\s+against', re.I)
]

def filter_bias(response: str) -> str:
    """Detect and block political bias in output."""
    for pattern in BIAS_PATTERNS:
        if pattern.search(response):
            return "I am here to provide neutral civic information only. I cannot share political opinions or endorsements."
    return response
