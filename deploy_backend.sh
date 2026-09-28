#!/bin/bash
# Deploy podcast backend to Cloud Run

set -e

PROJECT_ID="regal-scholar-453620-r7"
SERVICE_NAME="podcast-backend"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Podcast Backend to Cloud Run..."

# Build and push Docker image
echo "📦 Building Docker image..."
cd podcast_backend
gcloud builds submit --tag ${IMAGE_NAME} --project ${PROJECT_ID}

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 900 \
    --max-instances 10 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
    --project ${PROJECT_ID}

# Note: You'll need to set OPENAI_API_KEY manually:
echo "⚠️  IMPORTANT: Set your OpenAI API key:"
echo "gcloud run services update ${SERVICE_NAME} --region=${REGION} --set-env-vars OPENAI_API_KEY=your_key_here"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --project=${PROJECT_ID} --format="value(status.url)")

echo "✅ Backend deployed successfully!"
echo "📍 Service URL: ${SERVICE_URL}"
echo ""
echo "🔧 Next step: Update Cloud Function with this URL:"
echo "   CLOUD_RUN_URL=${SERVICE_URL}"

cd ..