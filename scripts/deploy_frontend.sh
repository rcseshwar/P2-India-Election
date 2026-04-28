#!/bin/bash
# Deploy Election Buddy Frontend to Cloud Run
# Usage: ./scripts/deploy_frontend.sh

set -euo pipefail

PROJECT_ID="p2-india-election"
REGION="us-central1"
REPO_NAME="india-election"
SERVICE_NAME="election-buddy-ui"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"

echo "🚀 Deploying Election Buddy Frontend to Cloud Run..."

# Build and push Docker image
echo "🔨 Building Frontend Docker image..."
cd frontend
gcloud builds submit \
    --tag "$IMAGE:latest" \
    --project "$PROJECT_ID" \
    --timeout=1200

# Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE:latest" \
    --platform managed \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --allow-unauthenticated \
    --port 80 \
    --memory 512Mi \
    --cpu 0.5 \
    --min-instances 0 \
    --max-instances 2 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,MODEL_ID=gemini-1.5-flash,ALLOWED_ORIGINS=*,GOOGLE_GENAI_USE_VERTEXAI=FALSE,GOOGLE_API_KEY=YOUR_API_KEY_HERE" \
    --quiet

# Get the service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --format='value(status.url)')

echo ""
echo "✅ Frontend Deployment complete!"
echo "🌐 App URL: $SERVICE_URL"
echo ""
