"""Sub-agent definitions for Sauti ya Mwananchi."""

from google.adk.agents import LlmAgent
from src.agents.safety import IMMUTABLE_SAFETY_PREAMBLE

from src.tools.civic_rag import search_civic_knowledge

mwalimu = LlmAgent(
    name="mwalimu",
    instruction=IMMUTABLE_SAFETY_PREAMBLE + "\nYou are Mwalimu, the Civic Educator. Provide accurate information about the Kenyan Constitution and election laws. Use the 'search_civic_knowledge' tool for any legal or constitutional questions.",
    model="gemini-2.0-flash",
    tools=[search_civic_knowledge]
)

from src.tools.polling_stations import search_polling_stations

kiongozi = LlmAgent(
    name="kiongozi",
    instruction=IMMUTABLE_SAFETY_PREAMBLE + "\nYou are Kiongozi, the Polling Station Locator. Help users find where they should vote. Use the 'search_polling_stations' tool to look up details based on user input.",
    model="gemini-2.0-flash",
    tools=[search_polling_stations]
)

from src.tools.fact_check import search_verified_claims
from src.tools.vision import analyze_political_image

ukweli = LlmAgent(
    name="ukweli",
    instruction=IMMUTABLE_SAFETY_PREAMBLE + "\nYou are Ukweli, the Fact-Checker. Verify election-related claims and debunk misinformation. Use 'search_verified_claims' for text-based claims and 'analyze_political_image' if a user provides an image URL.",
    model="gemini-2.0-flash",
    tools=[search_verified_claims, analyze_political_image]
)

from src.tools.election_day import get_election_day_step, get_voter_rights_summary

mwenza = LlmAgent(
    name="mwenza",
    instruction=IMMUTABLE_SAFETY_PREAMBLE + "\nYou are Mwenza, the Election Day Companion. Guide users through the step-by-step voting process. Use 'get_election_day_step' for specific process questions and 'get_voter_rights_summary' for rights at the station.",
    model="gemini-2.0-flash",
    tools=[get_election_day_step, get_voter_rights_summary]
)
