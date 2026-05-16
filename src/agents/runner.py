"""ADK Runner for Sauti ya Mwananchi."""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from src.agents.msaidizi import msaidizi
from src.gateway.normalizer import MessageEnvelope
from google.genai import types as genai_types
import logging

from src.guardrails.pii_scrubber import scrub_pii
from src.guardrails.injection_detector import detect_injection, INJECTION_REFUSAL
from src.guardrails.citation_validator import validate_citations
from src.guardrails.neutrality_filter import filter_bias

logger = logging.getLogger(__name__)

# Singleton session service and runner
_session_service = InMemorySessionService()
_runner = Runner(
    agent=msaidizi,
    app_name="sauti_ya_mwananchi",
    session_service=_session_service,
)

async def process_message(envelope: MessageEnvelope) -> str:
    """Process a message through the full guardrail + agent pipeline."""
    
    # -- 1. PII Scrubber (Pre-agent) --
    clean_text, pii_found = scrub_pii(envelope.text or "Habari")
    
    # -- 2. Injection Detector (Pre-agent) --
    if detect_injection(clean_text):
        return INJECTION_REFUSAL

    user_id = envelope.phone_hash
    session_id = envelope.session_id
    
    session = await _session_service.get_session(
        app_name="sauti_ya_mwananchi",
        user_id=user_id,
        session_id=session_id
    )
    
    if session is None:
        await _session_service.create_session(
            app_name="sauti_ya_mwananchi",
            user_id=user_id,
            session_id=session_id,
            state={"channel": envelope.channel}
        )
    
    user_content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=clean_text)]
    )

    response_parts = []
    async for event in _runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_parts.append(part.text)
                    
    raw_response = "".join(response_parts) if response_parts else "Samahani, sijakuelewa vizuri."
    
    # -- 3. Citation Validator (Post-agent) --
    validated = validate_citations(raw_response)
    
    # -- 4. Neutrality Filter (Post-agent) --
    final = filter_bias(validated)
    
    return final
