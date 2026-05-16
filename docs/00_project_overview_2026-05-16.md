---
title: "Sauti ya Mwananchi — Project Overview & Problem Statement"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Sauti ya Mwananchi — Project Overview

**Document ID:** SYM-DOC-00  
**Created:** 2026-05-16T09:30:00+03:00  
**Last Modified:** 2026-05-16T09:30:00+03:00  
**Status:** Draft

---

## 1. Project Name

**Sauti ya Mwananchi** (The Voice of the Citizen)

## 2. Problem Statement

Kenya's 2027 General Election approaches with a critical democratic gap: millions of eligible young citizens remain unregistered, uninformed, and disengaged. The #TukoKadi movement has energized Gen Z voter registration, but a fundamental problem persists — **the gap between registration and meaningful civic participation**.

Citizens who register face three compounding barriers:

1. **Information Asymmetry** — Constitutional rights, electoral processes, and candidate accountability data are locked in dense legal documents inaccessible to the average citizen.
2. **Misinformation Saturation** — Political propaganda circulates faster via WhatsApp and SMS than verified civic facts, eroding trust in democratic institutions.
3. **Last-Mile Access Failure** — On Election Day, citizens in rural and peri-urban areas cannot locate polling stations, understand ballot procedures, or access real-time guidance — especially those limited to USSD/SMS (no smartphones).

## 3. Solution

Sauti ya Mwananchi is an AI-powered multi-agent civic participation platform built on Google's Agent Development Kit (ADK) and Gemini. It meets citizens where they already are — **WhatsApp, SMS, and USSD** — delivering:

- Constitutional and civic education in English, Swahili, and Sheng
- Polling station location services
- Real-time misinformation fact-checking (including image analysis)
- Election Day step-by-step guidance optimized for feature phones

## 4. Core Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Political Neutrality** | Zero-opinion architecture; all outputs cite official sources only |
| **Privacy First** | Zero-retention policy; no voter data persists beyond session |
| **Accessibility** | USSD-first design ensures feature phone users are not excluded |
| **Multilingual** | Native English/Swahili/Sheng with automatic detection |
| **Citation Required** | Every civic claim must anchor to Constitution, IEBC, or Acts |

## 5. Target Users

- **Primary:** Kenyan citizens aged 18-35 (Gen Z / young millennials)
- **Secondary:** Rural and peri-urban voters with feature phones (USSD-only)
- **Tertiary:** Civic society organizations and voter education facilitators

## 6. Technology Stack

| Component | Technology |
|-----------|-----------|
| Core AI | Gemini 2.0 Flash / Pro via Vertex AI |
| Agent Framework | Google Agent Development Kit (ADK) — Python |
| Vision Analysis | Gemini Vision (multimodal) |
| RAG / Vector Search | Vertex AI Search (managed) or custom embeddings |
| Messaging Gateway | Africa's Talking (SMS, USSD, WhatsApp) |
| Deployment | Google Cloud Run (containerized) |
| CI/CD | Google Cloud Build |
| Container Registry | Google Artifact Registry |

## 7. Hackathon Alignment

This project targets the Google AI Hackathon requirements:

- **ADK Multi-Agent System** — Five specialized agents with orchestrator delegation
- **Gemini Foundation Models** — Used across all agents for reasoning, vision, and generation
- **Vertex AI Integration** — RAG engine, embeddings, model serving
- **Real-World Impact** — Directly addresses civic participation gap in Kenya's 2027 election cycle
- **Production Readiness** — Fully containerized, deployed on Cloud Run, integrated with live communication APIs

## 8. Document Index

| Doc ID | Title | Description |
|--------|-------|-------------|
| SYM-DOC-00 | Project Overview | This document |
| SYM-DOC-01 | System Architecture | Multi-agent orchestration flow and message routing |
| SYM-DOC-02 | Agent Definitions | Granular agent specs, prompts, and tool manifests |
| SYM-DOC-03 | Guardrails Framework | Jailbreak protection and political neutrality |
| SYM-DOC-04 | Deployment Blueprint | Dockerfile, Cloud Run, and DevOps scaffolding |
| SYM-DOC-05 | Execution Roadmap | Sprint-by-sprint hackathon plan |
| SYM-DOC-06 | README | Production-ready GitHub README.md |
