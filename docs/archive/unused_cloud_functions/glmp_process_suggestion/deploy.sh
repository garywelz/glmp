#!/bin/bash
# Deployment script for GLMP Process Suggestion Chat

set -e

PROJECT_ID="regal-scholar-453620-r7"
REGION="us-central1"
FUNCTION_NAME="glmp_process_suggestion"
BUCKET_NAME="regal-scholar-453620-r7-podcast-storage"

echo "🚀 Deploying GLMP Process Suggestion Chat..."
echo ""

if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from cloud-functions/glmp_process_suggestion/"
    exit 1
fi

gcloud functions deploy ${FUNCTION_NAME} \
  --gen2 \
  --runtime python311 \
  --region ${REGION} \
  --source . \
  --entry-point glmp_process_suggestion \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=${PROJECT_ID},BUCKET_NAME=${BUCKET_NAME} \
  --timeout 540s \
  --memory 1024Mi \
  --max-instances 10 \
  --min-instances 0

echo ""
echo "✅ Deployment complete!"
echo ""



