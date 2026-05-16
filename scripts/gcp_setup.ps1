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
