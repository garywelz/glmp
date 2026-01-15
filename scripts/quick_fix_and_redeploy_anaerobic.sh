#!/bin/bash
# Quick fix and redeploy for anaerobic respiration with aggressive cache clearing

set -e

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_FILE="processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "🔍 Checking local file..."
if [ ! -f "$PROCESS_FILE" ]; then
    echo "❌ File not found: $PROCESS_FILE"
    exit 1
fi

echo "✅ File found. Checking Mermaid syntax..."
MERMAID=$(jq -r '.mermaid' "$PROCESS_FILE")
COLON_COUNT=$(echo "$MERMAID" | grep -o ':' | wc -l)
QUOTED_COLON_COUNT=$(echo "$MERMAID" | grep -o '\["[^"]*:[^"]*"\]' | wc -l)

echo "   Total colons: $COLON_COUNT"
echo "   Quoted colons: $QUOTED_COLON_COUNT"

echo ""
echo "📤 Deploying to GCS with NO-CACHE headers..."
gsutil -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
    cp "$PROCESS_FILE" "$BUCKET/$GCS_PATH"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🧪 Test URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration&t=$(date +%s)"
echo ""
echo "⚠️  IMPORTANT: Use incognito mode or clear browser cache completely!"

