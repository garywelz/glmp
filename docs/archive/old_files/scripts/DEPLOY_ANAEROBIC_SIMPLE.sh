#!/bin/bash
# Simple deployment command for anaerobic respiration

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
LOCAL_FILE="processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "Deploying $LOCAL_FILE to $BUCKET/$GCS_PATH"
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
    cp "$LOCAL_FILE" "$BUCKET/$GCS_PATH"

echo ""
echo "✅ Done! Test URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration"

