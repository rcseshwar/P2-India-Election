#!/bin/bash
# Deploy Election Buddy to Cloud Run
# Usage: ./scripts/deploy.sh

set -euo pipefail

PROJECT_ID="p2-india-election"
REGION="us-central1"
REPO_NAME="india-election"
SERVICE_NAME="election-buddy-api"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"

echo "🚀 Deploying Election Buddy to Cloud Run..."

# Build and push Docker image
echo "🔨 Building Docker image..."
cd backend
gcloud builds submit \
    --tag "$IMAGE:latest" \
    --project "$PROJECT_ID" \
    --timeout=600

# Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE:latest" \
    --platform managed \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 5 \
    --timeout 300 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,MODEL_ID=gemini-2.0-flash-001,ALLOWED_ORIGINS=*" \
    --quiet

# Get the service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --format='value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo "❤️  Health check: $SERVICE_URL/health"
echo "📚 API docs: $SERVICE_URL/docs"
echo ""
echo "Next: Update frontend/.env with VITE_API_URL=$SERVICE_URL"
