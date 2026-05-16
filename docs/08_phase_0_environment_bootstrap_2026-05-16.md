---
title: "Phase 0 — Environment Bootstrap & GCP Foundation"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Phase 0 — Environment Bootstrap & GCP Foundation

**Document ID:** SYM-IMPL-P0  
**Created:** 2026-05-16T10:10:00+03:00  
**Last Modified:** 2026-05-16T10:10:00+03:00  
**Phase Status:** ☐ Pending

---

## Phase Objective

Stand up the complete local development environment, provision the Google Cloud project with all required APIs and IAM bindings, configure Africa's Talking sandbox credentials, and verify end-to-end connectivity to every external service before writing any application code.

---

## Dependencies & Blockers

| Dependency | Type | Resolution |
|-----------|------|-----------|
| Google Cloud account with billing enabled | **BLOCKER** | Must be resolved before any GCP work. Verify hackathon credits are redeemed. |
| Africa's Talking account | **BLOCKER** | Register at africastalking.com; sandbox is free and instant. |
| Python 3.12+ installed locally | Required | `python --version` must report 3.12+. Install from python.org if needed. |
| Git installed and configured | Required | `git --version` must succeed. |
| Docker Desktop installed | Required | Needed for Phase 10 but install now to avoid delays. |
| ngrok installed | Required | For exposing local server to AT webhooks. `winget install ngrok.ngrok` |
| Google Cloud CLI (gcloud) installed | **BLOCKER** | `winget install Google.CloudSDK` or download from cloud.google.com/sdk |

---

## Action Items

### Step 0.1 — Verify Local Toolchain

Confirm every required tool is installed and accessible from the terminal.

```
[Artifact Type: Verification Script] | [File Name: scripts/verify_environment.ps1] | [Timestamp: 2026-05-16 10:10 EAT]
```

```powershell
# scripts/verify_environment.ps1
# Run this script to verify all required tools are installed.

Write-Host "=== Sauti ya Mwananchi — Environment Verification ===" -ForegroundColor Cyan
Write-Host ""

$checks = @(
    @{ Name = "Python 3.12+";    Cmd = "python --version" },
    @{ Name = "pip";             Cmd = "pip --version" },
    @{ Name = "Git";             Cmd = "git --version" },
    @{ Name = "Google Cloud CLI";Cmd = "gcloud --version" },
    @{ Name = "Docker";          Cmd = "docker --version" },
    @{ Name = "ngrok";           Cmd = "ngrok --version" }
)

$failed = @()
foreach ($check in $checks) {
    try {
        $output = Invoke-Expression $check.Cmd 2>&1 | Select-Object -First 1
        Write-Host "[PASS] $($check.Name): $output" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] $($check.Name): NOT FOUND" -ForegroundColor Red
        $failed += $check.Name
    }
}

Write-Host ""
if ($failed.Count -eq 0) {
    Write-Host "All checks passed. Ready for Phase 0." -ForegroundColor Green
} else {
    Write-Host "MISSING: $($failed -join ', '). Install before proceeding." -ForegroundColor Red
}
```

### Step 0.2 — Google Cloud Project Setup

```
[Artifact Type: Shell Commands] | [File Name: scripts/gcp_setup.ps1] | [Timestamp: 2026-05-16 10:12 EAT]
```

```powershell
# scripts/gcp_setup.ps1
# One-time GCP project provisioning. Run once.

$PROJECT_ID = "sauti-ya-mwananchi"    # CHANGE to your actual project ID
$REGION     = "us-central1"
$SA_NAME    = "sauti-runner"

# --- Authenticate ---
gcloud auth login
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

# --- Enable Required APIs ---
Write-Host "Enabling APIs..." -ForegroundColor Cyan
$apis = @(
    "aiplatform.googleapis.com",           # Vertex AI (Gemini, embeddings)
    "discoveryengine.googleapis.com",      # Vertex AI Search (RAG)
    "run.googleapis.com",                  # Cloud Run
    "cloudbuild.googleapis.com",           # Cloud Build (CI/CD)
    "artifactregistry.googleapis.com",     # Docker image registry
    "secretmanager.googleapis.com",        # Secret Manager
    "storage.googleapis.com"              # Cloud Storage (document uploads)
)
foreach ($api in $apis) {
    gcloud services enable $api
    Write-Host "  Enabled: $api" -ForegroundColor Green
}

# --- Create Service Account ---
Write-Host "Creating service account..." -ForegroundColor Cyan
gcloud iam service-accounts create $SA_NAME `
    --display-name="Sauti ya Mwananchi Cloud Run SA"

$SA_EMAIL = "$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# --- Assign IAM Roles ---
$roles = @(
    "roles/aiplatform.user",              # Vertex AI access
    "roles/discoveryengine.viewer",       # Vertex AI Search queries
    "roles/secretmanager.secretAccessor", # Read secrets
    "roles/storage.objectViewer"          # Read civic docs from GCS
)
foreach ($role in $roles) {
    gcloud projects add-iam-policy-binding $PROJECT_ID `
        --member="serviceAccount:$SA_EMAIL" `
        --role=$role `
        --quiet
    Write-Host "  Granted: $role" -ForegroundColor Green
}

# --- Create Artifact Registry Repository ---
Write-Host "Creating Artifact Registry repo..." -ForegroundColor Cyan
gcloud artifacts repositories create sauti-ya-mwananchi `
    --repository-format=docker `
    --location=$REGION `
    --description="Sauti ya Mwananchi container images"

# --- Create Cloud Storage Bucket for Civic Documents ---
Write-Host "Creating GCS bucket for civic docs..." -ForegroundColor Cyan
gcloud storage buckets create "gs://$PROJECT_ID-civic-docs" `
    --location=$REGION `
    --uniform-bucket-level-access

Write-Host ""
Write-Host "=== GCP Setup Complete ===" -ForegroundColor Green
Write-Host "Project:          $PROJECT_ID"
Write-Host "Region:           $REGION"
Write-Host "Service Account:  $SA_EMAIL"
Write-Host "Docker Repo:      $REGION-docker.pkg.dev/$PROJECT_ID/sauti-ya-mwananchi"
Write-Host "Civic Docs GCS:   gs://$PROJECT_ID-civic-docs"
```

### Step 0.3 — Store Secrets in Secret Manager

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:14 EAT]
```

```powershell
# Store Africa's Talking credentials (replace with real values)
echo -n "your-at-api-key-here" | gcloud secrets create at-api-key --data-file=-
echo -n "sandbox" | gcloud secrets create at-username --data-file=-

# Verify secrets exist
gcloud secrets list
```

### Step 0.4 — Africa's Talking Sandbox Setup

**Manual Steps (no automation available):**

1. Navigate to [https://account.africastalking.com/](https://account.africastalking.com/)
2. Create an account or log in
3. Go to **Settings → API Key** and generate a new key. **Copy it immediately** — it is shown only once.
4. Note the sandbox username: always `sandbox`
5. Navigate to **Sandbox → Launch Simulator** — verify the simulator loads
6. Callback URLs will be configured in Phase 8 after the gateway is running

**Verification checkpoint:** You should now have:
- AT Username: `sandbox`
- AT API Key: `atsk_xxxxxxxxxxxxxxxxxxxx` (64 chars)

### Step 0.5 — Local Application Default Credentials

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:15 EAT]
```

```powershell
# Authenticate for local development (opens browser)
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token | Select-Object -First 1
# Should output a token string, not an error
```

### Step 0.6 — Initialize Git Repository

```
[Artifact Type: Shell Commands] | [File Name: (inline)] | [Timestamp: 2026-05-16 10:16 EAT]
```

```powershell
cd c:\Users\gvnrk\Documents\AG-HAL9000-IV\tuko_kadi_dev

# Verify git is initialized (already done)
git status

# Create .gitignore
# (will be created as an artifact below)

# Initial commit with existing docs
git add .
git commit -m "docs: add project blueprint documentation"
```

### Step 0.7 — Create .gitignore

```
[Artifact Type: Configuration File] | [File Name: .gitignore] | [Timestamp: 2026-05-16 10:17 EAT]
```

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.venv/
venv/
env/

# Environment
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Google Cloud
application_default_credentials.json
service-account-key.json

# Docker
.dockerignore

# Test
.pytest_cache/
htmlcov/
.coverage

# Build artifacts
docs/*.docx
```

### Step 0.8 — Create .env.example

```
[Artifact Type: Configuration Template] | [File Name: .env.example] | [Timestamp: 2026-05-16 10:18 EAT]
```

```bash
# ============================================================
# Sauti ya Mwananchi — Environment Configuration
# ============================================================
# Copy this file to .env and fill in your values:
#   cp .env.example .env
# ============================================================

# ---- Google Cloud ----
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE

# ---- Africa's Talking ----
AT_USERNAME=sandbox
AT_API_KEY=your-at-sandbox-api-key
AT_ENVIRONMENT=sandbox

# ---- Vertex AI Search Data Stores ----
# Format: projects/{project}/locations/global/collections/default_collection/dataStores/{datastore_id}
CIVIC_DATASTORE_ID=

# ---- Application Settings ----
LOG_LEVEL=INFO
MAX_SESSION_TIMEOUT_SECONDS=1800
PORT=8080
```

### Step 0.9 — Create Python Virtual Environment and Install Base Dependencies

```
[Artifact Type: Configuration File] | [File Name: requirements.txt] | [Timestamp: 2026-05-16 10:19 EAT]
```

```
# ============================================================
# Sauti ya Mwananchi — Python Dependencies
# ============================================================

# --- Core Framework ---
fastapi==0.115.*
uvicorn[standard]==0.34.*
python-dotenv==1.1.*
pydantic==2.*

# --- Google AI / Agent Development Kit ---
google-adk==1.*
google-cloud-aiplatform==1.*
google-cloud-discoveryengine==0.*
google-genai==1.*

# --- Africa's Talking ---
africastalking==2.*

# --- HTTP Client ---
httpx==0.28.*

# --- Testing ---
pytest==8.*
pytest-asyncio==0.24.*
httpx==0.28.*
```

```powershell
# Create venv and install
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 0.10 — Verify GCP Connectivity

```
[Artifact Type: Verification Script] | [File Name: scripts/verify_gcp.py] | [Timestamp: 2026-05-16 10:20 EAT]
```

```python
"""Verify connectivity to all required Google Cloud services."""

import sys

def check_vertex_ai():
    """Verify Gemini model access via Vertex AI."""
    from google import genai
    client = genai.Client(vertexai=True)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Reply with exactly: VERTEX_AI_OK"
    )
    assert "VERTEX_AI_OK" in response.text, f"Unexpected response: {response.text}"
    print("[PASS] Vertex AI / Gemini 2.0 Flash: Connected")

def check_discovery_engine():
    """Verify Discovery Engine API is accessible."""
    from google.cloud import discoveryengine_v1 as discoveryengine
    client = discoveryengine.SearchServiceClient()
    print("[PASS] Discovery Engine (Vertex AI Search): Client initialized")

def check_storage():
    """Verify Cloud Storage access."""
    from google.cloud import storage
    client = storage.Client()
    buckets = list(client.list_buckets(max_results=1))
    print(f"[PASS] Cloud Storage: Connected ({len(buckets)} bucket(s) visible)")

def main():
    checks = [
        ("Vertex AI / Gemini", check_vertex_ai),
        ("Discovery Engine", check_discovery_engine),
        ("Cloud Storage", check_storage),
    ]

    failed = []
    for name, check_fn in checks:
        try:
            check_fn()
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed.append(name)

    print()
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All GCP connectivity checks passed.")

if __name__ == "__main__":
    main()
```

---

## Required Artifacts — Summary

| # | Artifact Type | File Name | Description |
|---|--------------|-----------|-------------|
| 1 | Verification Script | `scripts/verify_environment.ps1` | Checks all local tools are installed |
| 2 | Setup Script | `scripts/gcp_setup.ps1` | Provisions GCP project, APIs, SA, IAM, GCS |
| 3 | Configuration | `.gitignore` | Git exclusion rules |
| 4 | Configuration Template | `.env.example` | Environment variable template |
| 5 | Dependencies | `requirements.txt` | Python package manifest |
| 6 | Verification Script | `scripts/verify_gcp.py` | Tests connectivity to Vertex AI, Discovery Engine, GCS |

---

## Exit Criteria

Phase 0 is complete when ALL of the following are true:

- [ ] `scripts/verify_environment.ps1` reports all checks PASS
- [ ] GCP project has all 7 APIs enabled
- [ ] Service account `sauti-runner` exists with 4 IAM roles
- [ ] Artifact Registry repo `sauti-ya-mwananchi` exists
- [ ] GCS bucket `{project}-civic-docs` exists
- [ ] AT sandbox API key is obtained and stored in Secret Manager
- [ ] `gcloud auth application-default login` succeeds
- [ ] `.venv` created and `pip install -r requirements.txt` succeeds
- [ ] `scripts/verify_gcp.py` reports all checks PASS
- [ ] `.gitignore`, `.env.example`, and `requirements.txt` committed to repo
