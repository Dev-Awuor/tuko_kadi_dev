---
title: "Sauti ya Mwananchi — Production README"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# README.md (Production-Ready)

**Document ID:** SYM-DOC-06  
**Created:** 2026-05-16T09:30:00+03:00  
**Last Modified:** 2026-05-16T09:30:00+03:00

The content below should be copied directly to the repository's `README.md` file.

---

<!-- BEGIN README CONTENT -->

# 🗳️ Sauti ya Mwananchi — The Civic Participation Agent

> **From registration to education, from questions to answers — meet every Kenyan voter where they are.**

Sauti ya Mwananchi ("Voice of the Citizen") is an AI-powered multi-agent civic participation platform that bridges the gap between voter registration and meaningful democratic engagement. Built for Kenya's 2027 election cycle, it delivers constitutional education, polling station lookup, misinformation fact-checking, and election day guidance through **WhatsApp, SMS, and USSD** — reaching citizens on smartphones and feature phones alike.

## 🎯 The Problem

Kenya's #TukoKadi movement has successfully mobilized millions of young voters to register. But registration is only step one. Citizens face:

- **Dense, inaccessible legal documents** — Constitutional rights exist on paper but aren't understood in practice
- **Rampant misinformation** — Fake election claims spread via WhatsApp faster than fact-checkers can respond
- **Last-mile failure** — On election day, citizens in rural areas can't find polling stations or understand ballot procedures, especially those limited to feature phones

**Sauti ya Mwananchi closes this gap with AI that speaks your language, on the device you already have.**

## 🏗️ Architecture

### Multi-Agent System (Google ADK)

```
                    ┌──────────────────────┐
                    │      MSAIDIZI        │
                    │   (Orchestrator)     │
                    │ Language Detection   │
                    │ Intent Routing       │
                    │ Input Sanitization   │
                    └──────┬───────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  MWALIMU    │ │  KIONGOZI   │ │   UKWELI    │
    │  (Educator) │ │  (Locator)  │ │  (Checker)  │
    │  RAG Search │ │  Geo Lookup │ │  Vision AI  │
    └─────────────┘ └─────────────┘ └─────────────┘
                           │
                    ┌──────▼──────┐
                    │   MWENZA    │
                    │ (Companion) │
                    │ USSD Guide  │
                    └─────────────┘
```

| Agent | Role | Key Tools |
|-------|------|-----------|
| **Msaidizi** | Front-door orchestrator. Detects language (EN/SW/Sheng), classifies intent, delegates to specialists | Intent classification, PII scrubbing |
| **Mwalimu** | Civic educator. Answers constitutional and electoral questions using RAG | Vertex AI Search over Constitution, Elections Act, IEBC docs |
| **Kiongozi** | Polling station locator. Finds where citizens vote | Geo-lookup against IEBC station database |
| **Ukweli** | Fact-checker. Verifies claims and analyzes images of political content | Gemini Vision, verified claims database |
| **Mwenza** | Election day companion. Step-by-step voting guide optimized for USSD | Election procedure database, USSD menu builder |

### Technology Stack

| Layer | Technology |
|-------|-----------|
| AI Framework | Google Agent Development Kit (ADK) |
| Foundation Model | Gemini 2.0 Flash / Pro via Vertex AI |
| Vision | Gemini Vision (multimodal) |
| RAG | Vertex AI Search |
| Messaging | Africa's Talking (SMS, USSD, WhatsApp) |
| Runtime | FastAPI on Google Cloud Run |
| CI/CD | Google Cloud Build + Artifact Registry |

## 🚀 Local Development Quickstart

### Prerequisites

- Python 3.12+
- Google Cloud project with billing enabled
- Google Cloud CLI (`gcloud`) installed and authenticated
- Africa's Talking sandbox account

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/tuko_kadi_dev.git
cd tuko_kadi_dev

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GCP project ID and AT sandbox credentials

# Authenticate with Google Cloud
gcloud auth application-default login

# Run the application
uvicorn src.main:app --reload --port 8080
```

### Testing with Africa's Talking Sandbox

```bash
# In a separate terminal, expose your local server
ngrok http 8080

# Then configure your AT sandbox callbacks:
# SMS:  https://your-ngrok-id.ngrok.io/webhook/sms
# USSD: https://your-ngrok-id.ngrok.io/webhook/ussd

# Use the AT Sandbox Simulator to send test messages
```

### Running Tests

```bash
pytest tests/ -v
```

## ☁️ Production Deployment (Cloud Run)

```bash
# One-command deployment via Cloud Build
gcloud builds submit --config=cloudbuild.yaml

# Or manually:
gcloud run deploy sauti-ya-mwananchi \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

After deployment, update your Africa's Talking production callback URLs to point to the Cloud Run service URL.

## 🛡️ Data Handling, Privacy & Political Neutrality

### Zero-Retention Privacy Policy

- **No personal data is stored.** Phone numbers are SHA-256 hashed for session management only.
- **No conversation logs are persisted.** All sessions exist in memory and are destroyed on timeout or container restart.
- **PII is scrubbed on input.** National ID numbers, phone numbers, and passport numbers are automatically redacted before reaching any AI agent.

### Political Neutrality Guarantee

Sauti ya Mwananchi is architecturally incapable of political bias:

1. **System-level constraints** — Every agent carries an immutable safety preamble that cannot be overridden by user input
2. **Citation-only outputs** — All civic claims must cite the Constitution, Elections Act, or IEBC sources. Ungrounded claims are blocked.
3. **Adversarial testing** — The system is tested against 8 categories of jailbreak attacks including role-play injection, hypothetical framing, and multilingual evasion
4. **No training on political content** — Agents use RAG over official documents only; they never generate political opinions from training data

### What the System Will NEVER Do

- ❌ Recommend a candidate, party, or political position
- ❌ Predict election outcomes or discuss polls
- ❌ Store voter registration numbers or personal data
- ❌ Impersonate a government official or IEBC representative
- ❌ Generate civic information without a verified source citation

## 👥 Team

| Role | Name | Responsibility |
|------|------|---------------|
| Lead Architect | *[Name]* | System design, multi-agent orchestration |
| AI Engineer | *[Name]* | Agent prompts, RAG pipeline, Gemini Vision |
| Backend Engineer | *[Name]* | FastAPI gateway, AT integration, Cloud Run |
| Civic Data Lead | *[Name]* | Constitution/IEBC data curation, fact-check DB |
| QA & Security | *[Name]* | Jailbreak testing, guardrails, privacy audit |

## 📄 License

This project is built for the Google AI Hackathon — TukoKadi Challenge. License TBD.

<!-- END README CONTENT -->
