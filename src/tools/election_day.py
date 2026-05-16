"""Election day procedure and voter rights tools."""

import json
import os

def get_election_day_step(step_number: int) -> str:
    """Get detailed instructions for a specific step in the voting process.
    
    Args:
        step_number: The step (1-6) to retrieve.
    
    Returns:
        The title and instructions for that step.
    """
    data_path = os.path.join("data", "election_day_steps.json")
    if not os.path.exists(data_path):
        return "Election day guide not found."

    with open(data_path, "r") as f:
        steps = json.load(f)

    for s in steps:
        if s["step"] == step_number:
            return f"Step {s['step']}: {s['title']}\n{s['description']}"

    return "Invalid step number. Please choose between 1 and 6."

def get_voter_rights_summary() -> str:
    """Get a summary of voter rights at the polling station."""
    return "You have the right to secret ballot, assistance if disabled, and a peaceful voting environment. [Source: CoK-2010, Article 38]"
