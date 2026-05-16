"""Search tool for verified election claims."""

import json
import os

def search_verified_claims(claim_query: str) -> str:
    """Verify an election-related claim against a database of facts.
    
    Args:
        claim_query: The claim or rumor to check.
    
    Returns:
        A verdict (TRUE/FALSE/UNVERIFIED) with a correction and source.
    """
    data_path = os.path.join("data", "verified_claims.json")
    if not os.path.exists(data_path):
        return "Fact-check database not found."

    with open(data_path, "r") as f:
        claims = json.load(f)

    query = claim_query.lower()
    for c in claims:
        if query in c["claim"].lower() or c["claim"].lower() in query:
            return f"Verdict: {c['verdict']}\nCorrection: {c['correction']}\nSource: {c['source']}"

    return "UNVERIFIED. I could not find a verified record for this specific claim. Please check the official IEBC portal (iebc.or.ke)."
