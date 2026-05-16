---
title: "Sauti ya Mwananchi — System Architecture & Multi-Agent Orchestration"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# System Architecture & Multi-Agent Orchestration Flow

**Document ID:** SYM-DOC-01  
**Created:** 2026-05-16T09:30:00+03:00  
**Last Modified:** 2026-05-16T09:30:00+03:00  
**Status:** Draft

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CITIZEN INTERFACE LAYER                       │
│  ┌───────────┐  ┌───────────┐  ┌──────────────┐                │
│  │ WhatsApp   │  │   SMS     │  │    USSD      │                │
│  │ (AT API)   │  │ (AT API)  │  │  (AT API)    │                │
│  └─────┬─────┘  └─────┬─────┘  └──────┬───────┘                │
│        │               │               │                         │
│        └───────────────┼───────────────┘                         │
│                        ▼                                         │
│         ┌──────────────────────────────┐                         │
│         │  Africa's Talking Webhooks   │                         │
│         │  POST /webhook/whatsapp      │                         │
│         │  POST /webhook/sms           │                         │
│         │  POST /webhook/ussd          │                         │
│         └──────────────┬───────────────┘                         │
└────────────────────────┼─────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 GATEWAY SERVICE (FastAPI)                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Input Normalizer                                        │    │
│  │  - Channel detection (whatsapp/sms/ussd)                 │    │
│  │  - Payload normalization to unified MessageEnvelope      │    │
│  │  - Media extraction (images from WhatsApp)               │    │
│  │  - Session ID derivation (phone_number + channel)        │    │
│  └─────────────────────┬───────────────────────────────────┘    │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ADK Runner (InMemorySessionService)                     │    │
│  │  - Creates/resumes session per phone+channel             │    │
│  │  - Invokes root agent (Msaidizi)                         │    │
│  │  - Collects response events                              │    │
│  └─────────────────────┬───────────────────────────────────┘    │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Output Formatter                                        │    │
│  │  - Channel-aware response formatting                     │    │
│  │  - USSD: ≤182 chars, menu-style, CON/END prefix         │    │
│  │  - SMS: ≤160 chars, plain text                           │    │
│  │  - WhatsApp: Rich markdown, links, up to 4096 chars      │    │
│  └─────────────────────┬───────────────────────────────────┘    │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Response Dispatcher                                     │    │
│  │  - Routes formatted response back via AT API             │    │
│  │  - USSD: direct HTTP response body                       │    │
│  │  - SMS/WhatsApp: AT SDK send call                        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT ORCHESTRATION LAYER (ADK)              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              MSAIDIZI (Root Orchestrator)                  │   │
│  │              model: gemini-2.0-flash                       │   │
│  │                                                            │   │
│  │  Responsibilities:                                         │   │
│  │  - Language detection (EN/SW/Sheng)                        │   │
│  │  - Intent classification                                   │   │
│  │  - Input sanitization (PII scrubbing)                      │   │
│  │  - Delegate to sub-agents via transfer_to_agent            │   │
│  │  - Synthesize final response in detected language          │   │
│  │                                                            │   │
│  │  sub_agents:                                               │   │
│  │  ┌────────────┬────────────┬───────────┬──────────────┐   │   │
│  │  │  Mwalimu   │  Kiongozi  │  Ukweli   │   Mwenza     │   │   │
│  │  │ (Educator) │ (Locator)  │ (Checker) │ (Companion)  │   │   │
│  │  └────────────┴────────────┴───────────┴──────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA & SERVICES LAYER                         │
│                                                                  │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────────┐  │
│  │ Vertex AI     │  │ Polling       │  │ Guardrail           │  │
│  │ Search (RAG)  │  │ Station DB    │  │ Validators          │  │
│  │               │  │ (Firestore/   │  │ (citation check,    │  │
│  │ - Constitution│  │  CSV lookup)  │  │  PII scrub,         │  │
│  │ - Elections   │  │               │  │  neutrality check)  │  │
│  │   Act 2011    │  │               │  │                     │  │
│  │ - IEBC Guides │  │               │  │                     │  │
│  └──────────────┘  └───────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Message Flow — Step by Step

### 2.1 Inbound Message Processing

1. **Citizen sends message** via WhatsApp, SMS, or dials USSD code
2. **Africa's Talking** delivers webhook POST to Cloud Run endpoint
3. **Gateway Service** normalizes the payload into a `MessageEnvelope`:

```python
@dataclass
class MessageEnvelope:
    """Unified message format across all channels."""
    session_id: str        # f"{phone_number}:{channel}"
    phone_number: str      # E.164 format
    channel: str           # "whatsapp" | "sms" | "ussd"
    text: str              # User message text
    media_url: str | None  # Image URL (WhatsApp only)
    ussd_session_id: str | None  # AT USSD session ID
    timestamp: str         # ISO 8601
```

4. **ADK Runner** creates or resumes a session using `session_id`
5. **Msaidizi (root agent)** receives the user input and begins processing

### 2.2 Orchestrator Routing Logic (Msaidizi)

Msaidizi uses LLM-driven delegation via ADK's native `transfer_to_agent` mechanism. The routing decision is based on **intent classification** performed in the system prompt:

**Intent Classification Matrix:**

| Intent Category | Keywords / Signals | Target Agent |
|----------------|-------------------|--------------|
| Civic Education | "constitution", "rights", "how to vote", "katiba", "haki" | Mwalimu |
| Polling Station | "polling station", "where do I vote", "kituo", location queries | Kiongozi |
| Fact Check | "is this true", "verify", "fake news", image attachment | Ukweli |
| Election Day | "election day", "ballot", "queue", "siku ya uchaguzi" | Mwenza |
| General / Greeting | greetings, unclear intent, help requests | Msaidizi (self-handle) |

**Anti-Loop Safeguards:**

1. **Max delegation depth = 1** — Sub-agents cannot delegate to other sub-agents; they must return to Msaidizi
2. **Session state tracking** — `state["last_agent"]` and `state["delegation_count"]` are checked before each transfer
3. **Fallback rule** — If `delegation_count > 3` in a single session turn, Msaidizi responds directly with a help menu
4. **Sub-agent `output_key`** — Each sub-agent writes its response to a named output key, which Msaidizi reads to compose the final response

### 2.3 Agent-to-Agent Communication Protocol

ADK uses **shared session state** (`session.state`) as the inter-agent communication bus. Here is the state schema:

```python
# Session state keys used for agent communication
STATE_SCHEMA = {
    # Set by Gateway
    "channel": str,           # "whatsapp" | "sms" | "ussd"
    "phone_hash": str,        # SHA-256 of phone (no raw PII in state)
    "detected_language": str,  # "en" | "sw" | "sheng"
    "media_url": str | None,  # Attached image URL

    # Set by Msaidizi
    "classified_intent": str,  # Intent category
    "delegation_count": int,   # Loop guard counter
    "last_agent": str,         # Name of last delegated agent

    # Set by Mwalimu
    "rag_sources": list[str],  # Citation sources used
    "rag_response": str,       # RAG-grounded answer

    # Set by Kiongozi
    "polling_station": dict,   # {name, county, constituency, lat, lng}

    # Set by Ukweli
    "fact_check_verdict": str, # "VERIFIED" | "FALSE" | "UNVERIFIED"
    "fact_check_sources": list[str],

    # Set by Mwenza
    "election_step": int,      # Current step in election day guide
    "ussd_menu_state": str,    # Current USSD menu position
}
```

### 2.4 USSD Stateless Transaction Handling

USSD requires special handling because Africa's Talking manages session state externally:

```
USSD Flow:
  User dials *384*123# → AT sends sessionId + text=""
  Gateway creates ADK session keyed to AT sessionId
  Msaidizi responds with main menu (CON prefix = keep session open)

  CON Welcome to Sauti ya Mwananchi
  1. Learn about your rights
  2. Find your polling station
  3. Check a claim
  4. Election day guide

  User selects "1" → AT sends sessionId + text="1"
  Gateway resumes ADK session, appends "1" as new user message
  Msaidizi routes to Mwalimu
  Mwalimu responds with civic education menu

  END prefix = terminate USSD session
```

## 3. Deployment Topology

```
Google Cloud Project
├── Cloud Run Service: sauti-ya-mwananchi
│   ├── Container: python:3.12-slim
│   ├── Port: 8080
│   ├── Min instances: 1 (avoid cold starts)
│   ├── Max instances: 10
│   ├── Memory: 1Gi
│   ├── CPU: 2
│   └── Environment Variables:
│       ├── GOOGLE_CLOUD_PROJECT
│       ├── GOOGLE_CLOUD_LOCATION (us-central1)
│       ├── AT_USERNAME
│       ├── AT_API_KEY
│       └── AT_ENVIRONMENT (sandbox | production)
│
├── Vertex AI Search Data Store
│   ├── kenya-constitution-ds
│   ├── elections-act-2011-ds
│   └── iebc-guidelines-ds
│
├── Artifact Registry
│   └── sauti-ya-mwananchi (Docker repo)
│
├── Cloud Build Trigger
│   └── On push to main → build + deploy
│
└── Secret Manager
    ├── at-api-key
    └── at-username
```

## 4. Network & Security Architecture

| Layer | Security Control |
|-------|-----------------|
| Ingress | Cloud Run allows unauthenticated (AT webhooks need public URL) |
| Webhook Auth | AT signature verification on all inbound webhooks |
| Secrets | All API keys in Secret Manager, mounted as env vars |
| PII | Phone numbers hashed (SHA-256) before entering session state |
| Egress | Only outbound to AT API and Vertex AI endpoints |
| TLS | Enforced end-to-end (Cloud Run default) |
| Session Data | InMemorySessionService — no persistence, wiped on container restart |
