---
title: "Sauti ya Mwananchi — Hackathon Execution Roadmap"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Step-by-Step Hackathon Execution Roadmap

**Document ID:** SYM-DOC-05  
**Created:** 2026-05-16T09:30:00+03:00  
**Last Modified:** 2026-05-16T09:30:00+03:00

---

## Sprint Overview

| Sprint | Duration | Focus | Exit Criteria |
|--------|----------|-------|---------------|
| Sprint 1 | Hours 0-4 | Foundation & Routing | Msaidizi routes intents to stub sub-agents |
| Sprint 2 | Hours 4-10 | Core Agent Logic | Mwalimu RAG + Ukweli Vision working end-to-end |
| Sprint 3 | Hours 10-16 | Channel Integration | AT SMS/USSD/WhatsApp webhooks live in sandbox |
| Sprint 4 | Hours 16-22 | Hardening & Deployment | Jailbreak tests pass, Cloud Run deployed |
| Sprint 5 | Hours 22-24 | Demo & Documentation | Video recorded, README polished, submission ready |

---

## Sprint 1: Foundation & Routing (Hours 0-4)

### Objectives
- GCP project setup and credit verification
- Project scaffolding with ADK
- Msaidizi orchestrator routing working locally

### Tasks

**Hour 0-1: Environment Setup**
- [ ] Verify Google Cloud credits are redeemed and billing is active
- [ ] Enable APIs: Vertex AI, Discovery Engine, Cloud Run, Artifact Registry, Secret Manager
- [ ] Install ADK: `pip install google-adk google-cloud-aiplatform`
- [ ] Create project structure (see Doc 04)
- [ ] Set up `.env` with sandbox credentials

**Hour 1-2: Msaidizi Orchestrator**
- [ ] Implement `src/agents/msaidizi.py` with system prompt from Doc 02
- [ ] Create stub sub-agents (mwalimu, kiongozi, ukweli, mwenza) that return placeholder responses
- [ ] Wire up agent hierarchy: `msaidizi.sub_agents = [mwalimu, kiongozi, ukweli, mwenza]`
- [ ] Test intent routing locally with ADK CLI: `adk run src/agents/`

**Hour 2-3: Gateway Service**
- [ ] Implement `src/main.py` with FastAPI
- [ ] Create webhook endpoints: `/webhook/sms`, `/webhook/ussd`, `/webhook/whatsapp`
- [ ] Implement `MessageEnvelope` normalizer
- [ ] Implement channel-aware output formatter

**Hour 3-4: Integration Test**
- [ ] Run gateway locally: `uvicorn src.main:app --reload`
- [ ] Test with curl: simulate AT webhook payloads
- [ ] Verify Msaidizi correctly classifies intents and delegates
- [ ] Write initial integration tests

### Sprint 1 Exit Criteria
- Msaidizi receives text input and routes to correct sub-agent
- Sub-agents return stub responses
- FastAPI gateway accepts webhook POSTs and returns formatted responses

---

## Sprint 2: Core Agent Logic (Hours 4-10)

### Objectives
- Mwalimu RAG pipeline operational with Constitution data
- Ukweli fact-checker with Gemini Vision integration
- Kiongozi polling station lookup functional
- Mwenza election day guide content ready

### Tasks

**Hour 4-6: Mwalimu RAG Setup**
- [ ] Upload civic documents to Cloud Storage: Constitution, Elections Act, IEBC guidelines
- [ ] Create Vertex AI Search data store and ingest documents
- [ ] Implement `search_civic_knowledge` tool using `google-cloud-discoveryengine`
- [ ] Implement `get_constitution_article` tool
- [ ] Replace Mwalimu stub with full system prompt + tools
- [ ] Test: "What are my rights as a voter?" → expects cited response

**Hour 6-8: Ukweli Fact-Checker + Vision**
- [ ] Implement `analyze_image_content` tool using Gemini Vision
- [ ] Implement `search_verified_claims` tool
- [ ] Create seed data: `data/verified_claims.json` with 10-15 common election myths
- [ ] Replace Ukweli stub with full agent
- [ ] Test: send image of fake election poster → expects analysis + verdict
- [ ] Test fallback: unknown claim → expects UNVERIFIED verdict

**Hour 8-9: Kiongozi Locator**
- [ ] Prepare `data/polling_stations.csv` with IEBC station data (county, constituency, ward, station name)
- [ ] Implement `find_polling_station` tool with CSV/Firestore lookup
- [ ] Implement `list_constituencies` tool
- [ ] Replace Kiongozi stub with full agent
- [ ] Test: "Where do I vote in Westlands?" → expects station list

**Hour 9-10: Mwenza Companion**
- [ ] Implement `get_election_day_step` tool with hardcoded election day steps
- [ ] Implement `get_voter_rights_at_station` tool
- [ ] Implement USSD-specific formatting logic (CON/END prefixes, 182 char limit)
- [ ] Replace Mwenza stub with full agent
- [ ] Test: "What do I do on election day?" → expects step-by-step guide

### Sprint 2 Exit Criteria
- All four sub-agents return substantive, tool-grounded responses
- Mwalimu cites Constitution/Acts in every civic response
- Ukweli processes images and returns verdicts
- End-to-end: user message → Msaidizi → sub-agent → cited response

---

## Sprint 3: Africa's Talking Integration (Hours 10-16)

### Objectives
- SMS callback working in AT sandbox
- USSD menu navigation working end-to-end
- WhatsApp (if available in sandbox) or simulated

### Tasks

**Hour 10-12: SMS Integration**
- [ ] Create AT sandbox app and generate API key
- [ ] Initialize AT SDK in `src/gateway/webhooks.py`
- [ ] Implement SMS callback handler (parse AT POST body)
- [ ] Implement SMS response sender via AT SDK
- [ ] Start ngrok tunnel: `ngrok http 8080`
- [ ] Configure AT sandbox SMS callback URL
- [ ] Test via AT sandbox simulator: send SMS → receive AI response

**Hour 12-14: USSD Integration**
- [ ] Implement USSD webhook handler with session management
- [ ] Build USSD menu tree:
  - Main menu → 4 service options
  - Each option → sub-menu with agent interaction
  - Back/exit navigation
- [ ] Implement CON/END prefix logic
- [ ] Implement 182-character response truncation
- [ ] Configure AT sandbox USSD callback URL
- [ ] Test via AT sandbox USSD simulator

**Hour 14-16: WhatsApp + Channel Polish**
- [ ] Implement WhatsApp webhook handler (if AT sandbox supports it)
- [ ] Handle media messages (image extraction for Ukweli)
- [ ] Implement rich formatting for WhatsApp responses
- [ ] Comprehensive channel-switching tests
- [ ] Error handling: AT API failures, timeouts, malformed payloads

### Sprint 3 Exit Criteria
- SMS: send message to sandbox number → receive AI civic response
- USSD: dial sandbox code → navigate menus → get civic information
- All channels route correctly through Msaidizi to sub-agents

---

## Sprint 4: Hardening & Deployment (Hours 16-22)

### Objectives
- All jailbreak tests pass
- Guardrail pipeline operational
- Deployed and accessible on Cloud Run

### Tasks

**Hour 16-18: Guardrails Implementation**
- [ ] Implement `src/guardrails/pii_scrubber.py`
- [ ] Implement `src/guardrails/citation_validator.py`
- [ ] Implement `src/guardrails/neutrality_filter.py`
- [ ] Wire guardrails into gateway pipeline (pre-agent + post-agent)
- [ ] Run all 8 jailbreak test cases from Doc 03
- [ ] Fix any failures; iterate on system prompts

**Hour 18-20: Testing Suite**
- [ ] Write `tests/test_jailbreak.py` — automated adversarial tests
- [ ] Write `tests/test_guardrails.py` — PII scrubbing, citation checks
- [ ] Write `tests/test_agents.py` — agent routing, tool invocation
- [ ] Write `tests/test_webhooks.py` — AT payload parsing
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Fix all failures

**Hour 20-22: Cloud Run Deployment**
- [ ] Build Docker image locally and test: `docker build -t sauti . && docker run -p 8080:8080 sauti`
- [ ] Push to Artifact Registry
- [ ] Deploy to Cloud Run via `cloudbuild.yaml` or manual `gcloud run deploy`
- [ ] Verify Cloud Run service is healthy
- [ ] Update AT sandbox callback URLs to Cloud Run service URL
- [ ] End-to-end test: SMS/USSD via AT sandbox → Cloud Run → AI response

### Sprint 4 Exit Criteria
- All jailbreak tests pass
- PII scrubbing confirmed working
- Docker container runs without errors
- Cloud Run service responds to AT webhooks

---

## Sprint 5: Demo & Submission (Hours 22-24)

### Objectives
- Demo video recorded
- README finalized
- Repository cleaned and submitted

### Tasks

**Hour 22-23: Demo Preparation**
- [ ] Prepare demo script covering all 5 agents
- [ ] Record 2-3 minute demo video showing:
  - SMS civic education query (Mwalimu)
  - USSD polling station lookup (Kiongozi)
  - WhatsApp image fact-check (Ukweli)
  - USSD election day guide (Mwenza)
  - Jailbreak attempt → blocked (Guardrails)
- [ ] Upload demo video

**Hour 23-24: Final Submission**
- [ ] Finalize README.md (see Doc 06)
- [ ] Clean up code: remove debug prints, commented code
- [ ] Verify all documentation in `docs/` folder
- [ ] Final `git push` to main branch
- [ ] Submit hackathon entry with:
  - Repository URL
  - Demo video URL
  - Cloud Run service URL
  - Brief project description

### Sprint 5 Exit Criteria
- Demo video showcases all key features
- README is polished and judge-ready
- Repository is clean and well-documented
- Submission form completed
