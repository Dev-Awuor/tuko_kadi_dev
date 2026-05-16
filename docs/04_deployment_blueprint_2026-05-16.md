---
title: "Sauti ya Mwananchi — Deployment Blueprint"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Local Setup & Google Cloud Run Deployment Blueprint

**Document ID:** SYM-DOC-04  
**Created:** 2026-05-16T09:30:00+03:00  
**Last Modified:** 2026-05-16T09:30:00+03:00

---

## 1. Project Structure

```
tuko_kadi_dev/
├── docs/                          # Project documentation
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI gateway entrypoint
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── msaidizi.py            # Orchestrator agent
│   │   ├── mwalimu.py             # Civic educator agent
│   │   ├── kiongozi.py            # Polling station locator
│   │   ├── ukweli.py              # Fact-checker agent
│   │   └── mwenza.py              # Election day companion
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── civic_rag.py           # RAG search tools
│   │   ├── polling_stations.py    # Station lookup tools
│   │   ├── fact_check.py          # Fact-check tools
│   │   ├── vision.py              # Gemini Vision tools
│   │   └── election_day.py        # Election day guide tools
│   ├── guardrails/
│   │   ├── __init__.py
│   │   ├── pii_scrubber.py        # PII detection & removal
│   │   ├── citation_validator.py  # Citation enforcement
│   │   └── neutrality_filter.py   # Political neutrality check
│   ├── gateway/
│   │   ├── __init__.py
│   │   ├── webhooks.py            # AT webhook handlers
│   │   ├── normalizer.py          # Input normalization
│   │   └── formatter.py           # Channel-aware output formatting
│   └── config.py                  # Environment & settings
├── data/
│   ├── constitution_kenya_2010.pdf
│   ├── elections_act_2011.pdf
│   ├── polling_stations.csv
│   └── verified_claims.json
├── tests/
│   ├── test_agents.py
│   ├── test_guardrails.py
│   ├── test_jailbreak.py
│   └── test_webhooks.py
├── Dockerfile
├── .dockerignore
├── .env.example
├── requirements.txt
├── cloudbuild.yaml
└── README.md
```

## 2. Dockerfile (Multi-Stage, Production-Optimized)

```dockerfile
# ============================================================
# Stage 1: Builder — install dependencies in isolated layer
# ============================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: Runtime — minimal production image
# ============================================================
FROM python:3.12-slim AS runtime

# Security: run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser -s /bin/false appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY src/ ./src/
COPY data/ ./data/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Cloud Run uses PORT env var (default 8080)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE ${PORT}

# Run with uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--workers", "2", \
     "--log-level", "info"]
```

## 3. Requirements File

```
# requirements.txt
# Core
fastapi==0.115.*
uvicorn[standard]==0.34.*
python-dotenv==1.1.*

# Google AI / ADK
google-adk==1.*
google-cloud-aiplatform==1.*
google-cloud-discoveryengine==0.*
google-genai==1.*

# Africa's Talking
africastalking==2.*

# Utilities
pydantic==2.*
httpx==0.28.*
```

## 4. Environment Variables

```bash
# .env.example
# ---- Google Cloud ----
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE

# ---- Africa's Talking ----
AT_USERNAME=sandbox
AT_API_KEY=your-at-api-key
AT_ENVIRONMENT=sandbox

# ---- Vertex AI Search Data Stores ----
CIVIC_DATASTORE_ID=projects/PROJECT/locations/global/collections/default_collection/dataStores/DS_ID

# ---- Application ----
LOG_LEVEL=INFO
MAX_SESSION_TIMEOUT_SECONDS=1800
```

## 5. Cloud Build Configuration (cloudbuild.yaml)

```yaml
# cloudbuild.yaml
steps:
  # Step 1: Build the Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/${_SERVICE_NAME}:${SHORT_SHA}'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/${_SERVICE_NAME}:latest'
      - '.'

  # Step 2: Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '--all-tags'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/${_SERVICE_NAME}'

  # Step 3: Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE_NAME}'
      - '--image'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/${_SERVICE_NAME}:${SHORT_SHA}'
      - '--region'
      - '${_REGION}'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '1Gi'
      - '--cpu'
      - '2'
      - '--min-instances'
      - '1'
      - '--max-instances'
      - '10'
      - '--set-env-vars'
      - 'GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${_REGION},AT_ENVIRONMENT=sandbox'
      - '--set-secrets'
      - 'AT_API_KEY=at-api-key:latest,AT_USERNAME=at-username:latest'
      - '--service-account'
      - '${_SERVICE_ACCOUNT}'

substitutions:
  _REGION: us-central1
  _REPO_NAME: sauti-ya-mwananchi
  _SERVICE_NAME: sauti-ya-mwananchi
  _SERVICE_ACCOUNT: sauti-runner@${PROJECT_ID}.iam.gserviceaccount.com

options:
  logging: CLOUD_LOGGING_ONLY
```

## 6. Manual Deployment Commands

```bash
# === ONE-TIME SETUP ===

# 1. Create Artifact Registry repository
gcloud artifacts repositories create sauti-ya-mwananchi \
  --repository-format=docker \
  --location=us-central1 \
  --description="Sauti ya Mwananchi container images"

# 2. Create service account with minimal permissions
gcloud iam service-accounts create sauti-runner \
  --display-name="Sauti ya Mwananchi Cloud Run SA"

# Grant Vertex AI access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:sauti-runner@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Grant Discovery Engine access (for Vertex AI Search)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:sauti-runner@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/discoveryengine.viewer"

# Grant Secret Manager access
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:sauti-runner@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# 3. Store secrets
echo -n "your-at-api-key" | gcloud secrets create at-api-key --data-file=-
echo -n "sandbox" | gcloud secrets create at-username --data-file=-

# === BUILD & DEPLOY ===

# Build image
gcloud builds submit --config=cloudbuild.yaml

# Or manual deploy:
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/sauti-ya-mwananchi/sauti-ya-mwananchi:latest .
docker push us-central1-docker.pkg.dev/$PROJECT_ID/sauti-ya-mwananchi/sauti-ya-mwananchi:latest
gcloud run deploy sauti-ya-mwananchi \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/sauti-ya-mwananchi/sauti-ya-mwananchi:latest \
  --region=us-central1 \
  --allow-unauthenticated
```

## 7. Local Development Setup

```bash
# 1. Clone and setup
git clone https://github.com/your-org/tuko_kadi_dev.git
cd tuko_kadi_dev

# 2. Create virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Authenticate with Google Cloud
gcloud auth application-default login

# 6. Run locally
uvicorn src.main:app --reload --port 8080

# 7. Expose for AT webhooks (separate terminal)
ngrok http 8080

# 8. Configure AT sandbox webhooks
# Go to https://account.africastalking.com/apps/sandbox
# Set callback URLs to your ngrok URL:
#   SMS: https://xxxx.ngrok.io/webhook/sms
#   USSD: https://xxxx.ngrok.io/webhook/ussd

# 9. Run tests
pytest tests/ -v
```
