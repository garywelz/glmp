#!/bin/bash
# Deploy Cloud Function for podcast generation

set -e

PROJECT_ID="regal-scholar-453620-r7"
FUNCTION_NAME="generate-podcast"
REGION="us-central1"

# Get Cloud Run URL (you'll need to update this after deploying the backend)
CLOUD_RUN_URL="https://podcast-backend-[HASH]-uc.a.run.app"  # Update this

echo "🚀 Deploying Cloud Function..."

if [ "$CLOUD_RUN_URL" = "https://podcast-backend-[HASH]-uc.a.run.app" ]; then
    echo "❌ ERROR: Please update CLOUD_RUN_URL in this script with the actual Cloud Run service URL"
    echo "   Run deploy_backend.sh first, then update this script with the returned URL"
    exit 1
fi

cd cloud_function

# Deploy function
gcloud functions deploy ${FUNCTION_NAME} \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --region ${REGION} \
    --memory 512MB \
    --timeout 540s \
    --set-env-vars "CLOUD_RUN_URL=${CLOUD_RUN_URL}" \
    --project ${PROJECT_ID}

echo "✅ Cloud Function deployed successfully!"
echo "📍 Function URL: https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME}"

cd ..