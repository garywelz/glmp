#!/bin/bash
# Deployment script for View Suggestions Handler

set -e

PROJECT_ID="regal-scholar-453620-r7"
REGION="us-central1"
FUNCTION_NAME="glmp_view_suggestions"
BUCKET_NAME="regal-scholar-453620-r7-podcast-storage"

echo "🚀 Deploying View Suggestions Handler..."
echo ""

if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from cloud-functions/glmp_view_suggestions/"
    exit 1
fi

gcloud functions deploy ${FUNCTION_NAME} \
  --gen2 \
  --runtime python311 \
  --region ${REGION} \
  --source . \
  --entry-point glmp_view_suggestions \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=${PROJECT_ID},BUCKET_NAME=${BUCKET_NAME} \
  --timeout 60s \
  --memory 256Mi \
  --max-instances 10 \
  --min-instances 0

echo ""
echo "✅ Deployment complete!"
echo ""


