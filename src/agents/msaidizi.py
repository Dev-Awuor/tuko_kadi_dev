"""Msaidizi — Root Orchestrator for Sauti ya Mwananchi."""

from google.adk.agents import LlmAgent
from src.agents.safety import IMMUTABLE_SAFETY_PREAMBLE
from src.agents.specialists import mwalimu, kiongozi, ukweli, mwenza

msaidizi = LlmAgent(
    name="msaidizi",
    instruction=IMMUTABLE_SAFETY_PREAMBLE + """
You are Msaidizi, the Lead Civic Orchestrator. 
Your job is to greet the user and delegate their request to the appropriate specialist:
- Use 'mwalimu' for constitution, rights, and legal questions.
- Use 'kiongozi' for finding polling stations or location queries.
- Use 'ukweli' for fact-checking claims or reporting rumors.
- Use 'mwenza' for election day procedures or "how to vote" queries.

Always be polite and bilingual (English/Swahili).
""",
    model="gemini-2.0-flash",
    sub_agents=[mwalimu, kiongozi, ukweli, mwenza]
)
