#!/bin/bash
# Deployment script for GLMP Feedback Hybrid System

set -e

PROJECT_ID="regal-scholar-453620-r7"
REGION="us-central1"
FUNCTION_NAME="glmp_feedback"
BUCKET_NAME="regal-scholar-453620-r7-podcast-storage"

echo "🚀 Deploying GLMP Feedback Hybrid System..."
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from cloud-functions/glmp_feedback/"
    exit 1
fi

# Deploy Cloud Function
echo "📦 Deploying Cloud Function..."
gcloud functions deploy ${FUNCTION_NAME} \
  --gen2 \
  --runtime python311 \
  --region ${REGION} \
  --source . \
  --entry-point glmp_feedback \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=${PROJECT_ID},BUCKET_NAME=${BUCKET_NAME} \
  --timeout 540s \
  --memory 512Mi \
  --max-instances 10 \
  --min-instances 0

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test the function:"
echo "   curl -X POST https://${REGION}-${PROJECT_ID}.cloudfunctions.net/${FUNCTION_NAME} \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"issueType\":\"test\",\"suggestion\":\"test\"}'"
echo ""
echo "2. Check logs:"
echo "   gcloud functions logs read ${FUNCTION_NAME} --gen2 --region ${REGION} --limit 50"
echo ""
echo "3. (Optional) Set up Cloud Scheduler for email processing"
echo "   See HYBRID_SYSTEM_README.md for details"
echo ""



