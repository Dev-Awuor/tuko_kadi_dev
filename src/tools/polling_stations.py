"""Fuzzy lookup tool for polling stations."""

import json
import os
from typing import List, Dict

def search_polling_stations(query: str) -> str:
    """Find a polling station by name, ward, or constituency.
    
    Args:
        query: The name of the place, ward, or constituency to look for.
    
    Returns:
        A list of matching polling stations or a request for more detail.
    """
    data_path = os.path.join("data", "polling_stations.json")
    if not os.path.exists(data_path):
        return "Polling station database not found."

    with open(data_path, "r") as f:
        stations = json.load(f)

    query = query.lower()
    matches = []
    for s in stations:
        if (query in s["station_name"].lower() or 
            query in s["ward"].lower() or 
            query in s["constituency"].lower()):
            matches.append(s)

    if not matches:
        return f"No polling stations found for '{query}'. Please try a different name or provide your County/Ward."

    result = "Found the following stations:\n"
    for m in matches[:3]:  # Limit for USSD brevity
        result += f"- {m['station_name']} ({m['ward']}, {m['constituency']})\n"
    
    if len(matches) > 3:
        result += "...and more. Please be more specific."
        
    return result
