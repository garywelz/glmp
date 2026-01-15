#!/bin/bash
# Deploy fixed anaerobic_respiration.json with tildes replaced by hyphens

set -euo pipefail

GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_FILE="./processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="${GCS_BUCKET}/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "📤 Deploying fixed anaerobic_respiration.json..."
echo "   File: ${PROCESS_FILE}"
echo "   Destination: ${GCS_PATH}"

# Verify no tildes remain
TILDE_COUNT=$(jq -r .mermaid "${PROCESS_FILE}" | grep -c '~' 2>/dev/null | tr -d '\n' || echo "0")
if [ "${TILDE_COUNT}" -gt 0 ] 2>/dev/null; then
    echo "⚠️  WARNING: ${TILDE_COUNT} tildes still found in Mermaid string!"
    echo "   Please run the tilde replacement fix first."
    exit 1
fi
echo "✅ Verified: No tildes in local file"

# Upload
gsutil -h "Content-Type:application/json" cp "${PROCESS_FILE}" "${GCS_PATH}"

# Force no-cache
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" "${GCS_PATH}"

# Verify server copy
echo ""
echo "🔍 Verifying server copy..."
SERVER_TILDES=$(curl -s "https://storage.googleapis.com/${GCS_BUCKET#gs://}/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json" \
    | jq -r .mermaid | grep -c '~' || echo "0")

if [ "${SERVER_TILDES}" = "0" ]; then
    echo "✅ Server copy verified: No tildes found"
else
    echo "⚠️  Server copy still has ${SERVER_TILDES} tildes"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🧪 Test URL (with cache-buster):"
echo "   https://storage.googleapis.com/${GCS_BUCKET#gs://}/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration&ts=$(date +%s)"
echo ""
echo "   ⏰ Wait 30-60 seconds for GCS propagation, then test in incognito mode."

