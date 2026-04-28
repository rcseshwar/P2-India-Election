#!/bin/bash
# Setup GCP resources for India Election Education Platform
# Usage: ./scripts/setup_gcp.sh

set -euo pipefail

PROJECT_ID="p2-india-election"
REGION="us-central1"
REPO_NAME="india-election"
SERVICE_NAME="election-buddy-api"

echo "🗳️  Setting up GCP resources for Election Buddy..."
echo "Project: $PROJECT_ID | Region: $REGION"

# Set project
gcloud config set project "$PROJECT_ID"

# Enable APIs
echo "📦 Enabling required APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    firestore.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com

# Create Firestore database (Native mode)
echo "🔥 Creating Firestore database..."
gcloud firestore databases create \
    --location="$REGION" \
    --type=firestore-native \
    2>/dev/null || echo "Firestore database already exists."

# Create Artifact Registry repo
echo "📦 Creating Artifact Registry repository..."
gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="India Election Education Platform images" \
    2>/dev/null || echo "Artifact Registry repo already exists."

# Grant Cloud Build permissions
echo "🔐 Setting up IAM permissions..."
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')

# Cloud Build service account permissions
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.user" \
    --quiet 2>/dev/null || true

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/datastore.user" \
    --quiet 2>/dev/null || true

echo ""
echo "✅ GCP setup complete!"
echo ""
echo "Next steps:"
echo "  1. Deploy backend: ./scripts/deploy.sh"
echo "  2. Or run locally: cd backend && pip install -r requirements.txt && python main.py"
