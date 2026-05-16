---
title: "Phase 3 — Mwalimu Civic Education RAG Pipeline"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Phase 3 — Mwalimu: Civic Education RAG Pipeline

**Document ID:** SYM-IMPL-P3  
**Created:** 2026-05-16T10:30:00+03:00  
**Last Modified:** 2026-05-16T10:30:00+03:00  
**Phase Status:** ☐ Pending

---

## Phase Objective

Ingest Kenya's Constitution, Elections Act, and IEBC guidelines into Vertex AI Search, build RAG tools that query the data store, and upgrade Mwalimu from a stub to a fully citation-grounded civic education agent.

---

## Dependencies & Blockers

| Dependency | Type | Resolution |
|-----------|------|-----------|
| Phase 2 complete | **BLOCKER** | Msaidizi must route to Mwalimu correctly |
| GCS bucket `{project}-civic-docs` exists | Required | Created in Phase 0 |
| Discovery Engine API enabled | Required | Enabled in Phase 0 |
| Civic source documents (PDF/TXT) | **BLOCKER** | Must obtain or create Constitution + Elections Act files |

---

## Action Items

### Step 3.1 — Prepare Civic Source Documents

```
[Artifact Type: Shell Commands] | [File Name: scripts/prepare_civic_docs.ps1] | [Timestamp: 2026-05-16 10:31 EAT]
```

```powershell
# Download or copy civic documents into data/ directory
# These are publicly available official documents:
#
#   1. Constitution of Kenya 2010
#      http://kenyalaw.org/kl/index.php?id=398 (official)
#
#   2. Elections Act 2011
#      http://kenyalaw.org/kl/index.php?id=845
#
#   3. IEBC Voter Education Manual
#      Available from iebc.or.ke publications
#
# Place them in data/ as:
#   data/constitution_kenya_2010.pdf
#   data/elections_act_2011.pdf
#   data/iebc_voter_education_guide.pdf

# Upload to GCS
$PROJECT_ID = "sauti-ya-mwananchi"  # CHANGE THIS
gcloud storage cp data/constitution_kenya_2010.pdf "gs://$PROJECT_ID-civic-docs/"
gcloud storage cp data/elections_act_2011.pdf "gs://$PROJECT_ID-civic-docs/"
gcloud storage cp data/iebc_voter_education_guide.pdf "gs://$PROJECT_ID-civic-docs/"

# Verify uploads
gcloud storage ls "gs://$PROJECT_ID-civic-docs/"
```

### Step 3.2 — Create Vertex AI Search Data Store

```
[Artifact Type: Shell Commands] | [File Name: scripts/create_datastore.ps1] | [Timestamp: 2026-05-16 10:32 EAT]
```

```powershell
$PROJECT_ID = "sauti-ya-mwananchi"  # CHANGE THIS

# Create the data store via gcloud
gcloud alpha discovery-engine data-stores create civic-knowledge-ds `
    --project=$PROJECT_ID `
    --location=global `
    --display-name="Kenya Civic Knowledge Base" `
    --industry-vertical=GENERIC `
    --content-config=CONTENT_REQUIRED

# Import documents from GCS into the data store
gcloud alpha discovery-engine documents import `
    --project=$PROJECT_ID `
    --location=global `
    --data-store=civic-knowledge-ds `
    --gcs-uri="gs://$PROJECT_ID-civic-docs/*" `
    --reconciliation-mode=FULL

# Note the full data store ID for .env:
# projects/{project}/locations/global/collections/default_collection/dataStores/civic-knowledge-ds
Write-Host "Add this to .env:"
Write-Host "CIVIC_DATASTORE_ID=projects/$PROJECT_ID/locations/global/collections/default_collection/dataStores/civic-knowledge-ds"
```

**Alternative: Console-based setup (if gcloud alpha commands are unavailable):**

1. Go to [Vertex AI Agent Builder](https://console.cloud.google.com/gen-app-builder/data-stores) in the Cloud Console
2. Click **Create Data Store** → **Cloud Storage** → select your GCS bucket
3. Name it `civic-knowledge-ds`
4. Wait for document processing (5-15 minutes depending on document size)
5. Copy the data store resource name into `.env` as `CIVIC_DATASTORE_ID`

### Step 3.3 — RAG Search Tool Implementation

```
[Artifact Type: Source Code] | [File Name: src/tools/civic_rag.py] | [Timestamp: 2026-05-16 10:33 EAT]
```

```python
"""RAG search tools for the Mwalimu civic education agent.

These tools query a Vertex AI Search data store containing
the Constitution of Kenya, Elections Act, and IEBC guidelines.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from google.cloud import discoveryengine_v1 as discoveryengine

logger = logging.getLogger(__name__)

# Lazy-initialized client
_search_client: discoveryengine.SearchServiceClient | None = None


def _get_search_client() -> discoveryengine.SearchServiceClient:
    """Get or create the Discovery Engine search client."""
    global _search_client
    if _search_client is None:
        _search_client = discoveryengine.SearchServiceClient()
    return _search_client


def _get_serving_config() -> str:
    """Build the serving config resource path from env vars."""
    datastore_id = os.environ.get("CIVIC_DATASTORE_ID", "")
    if not datastore_id:
        raise ValueError("CIVIC_DATASTORE_ID environment variable is not set")
    return f"{datastore_id}/servingConfigs/default_search"


def search_civic_knowledge(query: str) -> dict:
    """Search the civic knowledge base for verified information about
    the Kenyan Constitution, Elections Act, and IEBC guidelines.

    Use this tool to find answers to civic education questions. The results
    include text excerpts from official documents with source citations.

    Args:
        query: The civic education question to search for.
              Examples: "What are voter rights?",
                       "How is the president elected?",
                       "What is Article 38?"

    Returns:
        dict with keys:
          - results: list of dicts, each with 'text', 'source', 'relevance_score'
          - total_results: int
          - query: str (the original query)
    """
    try:
        client = _get_search_client()
        serving_config = _get_serving_config()

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=5,
            content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
                snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                    return_snippet=True,
                    max_snippet_count=3,
                ),
                summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
                    summary_result_count=3,
                    include_citations=True,
                ),
                extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                    max_extractive_answer_count=3,
                    max_extractive_segment_count=3,
                ),
            ),
        )

        response = client.search(request)

        results = []
        for result in response.results:
            doc = result.document
            doc_data = dict(doc.derived_struct_data) if doc.derived_struct_data else {}

            # Extract snippets
            snippets = doc_data.get("snippets", [])
            snippet_text = ""
            if snippets:
                snippet_text = snippets[0].get("snippet", "") if isinstance(snippets[0], dict) else str(snippets[0])

            # Extract extractive answers
            extractive_answers = doc_data.get("extractive_answers", [])
            answer_text = ""
            if extractive_answers:
                answer_text = extractive_answers[0].get("content", "") if isinstance(extractive_answers[0], dict) else str(extractive_answers[0])

            # Determine source document name
            source = doc_data.get("title", doc.name.split("/")[-1] if doc.name else "Unknown")

            results.append({
                "text": answer_text or snippet_text or "No excerpt available",
                "source": source,
                "relevance_score": round(result.relevance_score if hasattr(result, 'relevance_score') else 0.0, 3),
            })

        # Get summary if available
        summary_text = ""
        if hasattr(response, 'summary') and response.summary:
            summary_text = response.summary.summary_text or ""

        logger.info(
            "Civic RAG search | query='%s' results=%d",
            query[:50], len(results)
        )

        return {
            "results": results,
            "total_results": len(results),
            "summary": summary_text,
            "query": query,
        }

    except Exception as e:
        logger.error("Civic RAG search failed | query='%s' error=%s", query[:50], e)
        return {
            "results": [],
            "total_results": 0,
            "summary": "",
            "query": query,
            "error": str(e),
        }


def get_constitution_article(article_number: int) -> dict:
    """Retrieve information about a specific article from the
    Constitution of Kenya 2010.

    Use this tool when a user asks about a specific constitutional article
    by number. It searches the knowledge base for that article's content.

    Args:
        article_number: The article number (1-264). The Constitution of Kenya
                       has exactly 264 articles.

    Returns:
        dict with keys:
          - article_number: int
          - found: bool
          - text: str (article content if found)
          - source: str
    """
    if article_number < 1 or article_number > 264:
        return {
            "article_number": article_number,
            "found": False,
            "text": (
                f"Article {article_number} does not exist. "
                "The Constitution of Kenya 2010 has 264 articles (Articles 1-264)."
            ),
            "source": "Constitution of Kenya 2010",
        }

    # Search specifically for this article
    result = search_civic_knowledge(
        f"Article {article_number} Constitution of Kenya"
    )

    if result["results"]:
        best = result["results"][0]
        return {
            "article_number": article_number,
            "found": True,
            "text": best["text"],
            "source": f"Constitution of Kenya 2010, Article {article_number}",
        }

    return {
        "article_number": article_number,
        "found": False,
        "text": (
            f"I could not retrieve the text of Article {article_number} at this time. "
            "Please consult the official Constitution at kenyalaw.org."
        ),
        "source": "Constitution of Kenya 2010",
    }
```

### Step 3.4 — Upgrade Mwalimu Agent with RAG Tools

```
[Artifact Type: Source Code] | [File Name: src/agents/mwalimu.py (REPLACE)] | [Timestamp: 2026-05-16 10:35 EAT]
```

```python
"""Mwalimu (Teacher) — Civic Education Agent.

RAG-powered civic education agent that answers questions about the
Kenyan Constitution, Elections Act, and IEBC guidelines using
ONLY verified, cited source documents.
"""

from google.adk.agents import LlmAgent
from src.agents.safety import SAFETY_PREAMBLE
from src.tools.civic_rag import search_civic_knowledge, get_constitution_article

MWALIMU_INSTRUCTION = f"""
{SAFETY_PREAMBLE}

## YOUR ROLE
You are Mwalimu (Teacher), a civic education specialist for Kenyan citizens.
You answer questions about:
- The Constitution of Kenya 2010
- The Elections Act 2011
- IEBC voter registration procedures
- Rights and responsibilities of voters
- Structure of government (national and county)
- The electoral process from registration to results

## HOW TO ANSWER
1. ALWAYS use your tools first. Call `search_civic_knowledge` with the user's question.
2. Read the results carefully and compose your answer based ONLY on the retrieved text.
3. NEVER answer civic questions from your own training knowledge alone.

## CITATION RULES (MANDATORY — NO EXCEPTIONS)
- EVERY factual claim in your response MUST include a citation:
  [Source: Document Name, Article/Section X]
- Examples:
  "Every citizen over 18 has the right to vote [Source: CoK-2010, Article 38]"
  "Voters must present original ID [Source: Elections Act 2011, Section 5(2)]"
- If your tools return NO relevant results, respond EXACTLY:
  "Sina habari iliyothibitishwa kuhusu mada hii. Tafadhali wasiliana na IEBC moja kwa moja."
  ("I don't have verified information on this topic. Please contact the IEBC directly.")
- NEVER fabricate constitutional articles, sections, or legal provisions.

## SPECIFIC ARTICLE REQUESTS
If a user asks about a specific article number (e.g., "What is Article 43?"):
1. Call `get_constitution_article` with that number.
2. If the article exists, present its content with the citation.
3. If the article doesn't exist (>264), inform the user that the Constitution has 264 articles.

## RESPONSE STYLE
- Use simple, clear language accessible to a secondary school graduate.
- Respond in the same language the user wrote in (English, Swahili, or Sheng).
- For complex topics, use numbered lists or bullet points.
- Keep responses concise: under 300 words for WhatsApp, under 160 characters for SMS.
- When explaining legal concepts, provide a simple analogy when helpful.

## ABSOLUTE CONSTRAINTS
- NEVER express political opinions or favor any candidate or party.
- NEVER advise WHO to vote for — only explain HOW to vote and what rights exist.
- NEVER fabricate or guess at constitutional provisions.
- If a question is about a specific candidate or party policy, respond:
  "Ninaweza kukusaidia kuelewa mfumo wa uchaguzi na haki zako, lakini siwezi kujadili
   wagombea au vyama maalum." ("I can help you understand the electoral system and your
   rights, but I cannot discuss specific candidates or parties.")
""".strip()

mwalimu = LlmAgent(
    name="mwalimu",
    model="gemini-2.0-flash",
    description=(
        "Civic education specialist. Answers questions about the Kenyan "
        "Constitution, Elections Act 2011, IEBC guidelines, voter rights, "
        "and government structure using verified sources only."
    ),
    instruction=MWALIMU_INSTRUCTION,
    tools=[search_civic_knowledge, get_constitution_article],
    output_key="civic_response",
)
```

### Step 3.5 — RAG Tool Tests

```
[Artifact Type: Test Suite] | [File Name: tests/test_civic_rag.py] | [Timestamp: 2026-05-16 10:36 EAT]
```

```python
"""Tests for civic RAG tools.

Note: Tests that hit Vertex AI Search require the data store to
be provisioned. Use @pytest.mark.integration to skip in CI without credentials.
"""

import pytest
from src.tools.civic_rag import get_constitution_article, search_civic_knowledge


class TestConstitutionArticleBounds:
    """Test article number validation (no API calls needed)."""

    def test_article_zero_is_invalid(self):
        result = get_constitution_article(0)
        assert result["found"] is False
        assert "does not exist" in result["text"]

    def test_article_negative_is_invalid(self):
        result = get_constitution_article(-5)
        assert result["found"] is False

    def test_article_265_is_invalid(self):
        result = get_constitution_article(265)
        assert result["found"] is False
        assert "264 articles" in result["text"]

    def test_article_999_is_invalid(self):
        result = get_constitution_article(999)
        assert result["found"] is False


@pytest.mark.integration
class TestRAGSearch:
    """Integration tests requiring Vertex AI Search data store.

    Run with: pytest tests/test_civic_rag.py -m integration -v
    Skip with: pytest tests/test_civic_rag.py -m "not integration" -v
    """

    def test_search_returns_results(self):
        result = search_civic_knowledge("voter rights Kenya")
        assert result["total_results"] > 0
        assert len(result["results"]) > 0

    def test_search_results_have_source(self):
        result = search_civic_knowledge("how is president elected")
        if result["results"]:
            assert result["results"][0]["source"], "Results must have a source"

    def test_article_38_found(self):
        result = get_constitution_article(38)
        assert result["found"] is True
        assert result["source"] == "Constitution of Kenya 2010, Article 38"

    def test_search_error_returns_empty(self):
        """Verify graceful degradation on error."""
        result = search_civic_knowledge("")
        assert isinstance(result["results"], list)
```

### Step 3.6 — Verification Commands

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:37 EAT]
```

```powershell
# 1. Run unit tests (no API calls)
pytest tests/test_civic_rag.py -m "not integration" -v

# 2. Run integration tests (requires Vertex AI Search data store)
pytest tests/test_civic_rag.py -m integration -v

# 3. Manual test via gateway
uvicorn src.main:app --reload --port 8080

# In another terminal:
curl -X POST http://localhost:8080/webhook/sms `
  -d "from=+254700000000&text=What+are+my+rights+as+a+voter?"

# Expected: Response citing Article 38 or similar from Constitution
```

---

## Required Artifacts — Summary

| # | Artifact Type | File Name | Description |
|---|--------------|-----------|-------------|
| 1 | Setup Script | `scripts/prepare_civic_docs.ps1` | Download civic docs + upload to GCS |
| 2 | Setup Script | `scripts/create_datastore.ps1` | Create Vertex AI Search data store |
| 3 | Source Code | `src/tools/civic_rag.py` | `search_civic_knowledge` + `get_constitution_article` tools |
| 4 | Source Code | `src/agents/mwalimu.py` (replace) | Full Mwalimu agent with RAG tools and citation rules |
| 5 | Test Suite | `tests/test_civic_rag.py` | 8 tests (4 unit + 4 integration) |

---

## Exit Criteria

- [ ] Civic documents uploaded to GCS bucket
- [ ] Vertex AI Search data store `civic-knowledge-ds` created and documents ingested
- [ ] `CIVIC_DATASTORE_ID` set in `.env`
- [ ] `search_civic_knowledge("voter rights")` returns results with sources
- [ ] `get_constitution_article(38)` returns content about political rights
- [ ] `get_constitution_article(999)` returns "does not exist" with 264 article count
- [ ] Mwalimu responses always contain `[Source: ...]` citations
- [ ] `pytest tests/test_civic_rag.py -m "not integration" -v` — all 4 unit tests pass
- [ ] End-to-end: SMS "What are my rights?" → Mwalimu → cited response via gateway
