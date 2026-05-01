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
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,MODEL_ID=gemini-flash-latest,ALLOWED_ORIGINS=*,GOOGLE_GENAI_USE_VERTEXAI=FALSE,GOOGLE_API_KEY=AIzaSyD5Dxoiaz5iGSX3fI1t197O-F1m1AZ2MFc" \
    --quiet

# Get the backend service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --format='value(status.url)')

echo "Backend URL: $SERVICE_URL"

# Deploy Frontend
FRONTEND_SERVICE_NAME="election-buddy-ui"
FRONTEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$FRONTEND_SERVICE_NAME"

echo "🚀 Deploying Frontend to Cloud Run..."
cd ../frontend

echo "🔨 Building Frontend Docker image..."
gcloud builds submit \
    --tag "$FRONTEND_IMAGE:latest" \
    --project "$PROJECT_ID" \
    --timeout=600

echo "☁️  Deploying Frontend to Cloud Run..."
gcloud run deploy "$FRONTEND_SERVICE_NAME" \
    --image "$FRONTEND_IMAGE:latest" \
    --platform managed \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 5 \
    --timeout 300 \
    --set-env-vars "VITE_API_URL=$SERVICE_URL" \
    --quiet

FRONTEND_URL=$(gcloud run services describe "$FRONTEND_SERVICE_NAME" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --format='value(status.url)')

echo ""
echo "✅ Deployment complete!"
echo "🌐 Backend API URL: $SERVICE_URL"
echo "🌐 Frontend UI URL: $FRONTEND_URL"
echo "❤️  Health check: $SERVICE_URL/health"
echo "📚 API docs: $SERVICE_URL/docs"
echo ""
