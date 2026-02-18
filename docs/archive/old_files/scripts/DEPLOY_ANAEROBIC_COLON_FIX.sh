#!/bin/bash
# Deploy the quote-wrapped colon fix for anaerobic_respiration.json

set -e

GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_FILE="./processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
GCS_PATH="${GCS_BUCKET}/glmp-v2/processes/ecoli/ecoli_anaerobic_respiration.json"

echo "📤 Deploying colon fix for anaerobic_respiration.json..."
echo "   File: ${PROCESS_FILE}"
echo "   Destination: ${GCS_PATH}"

# Verify file exists
if [ ! -f "${PROCESS_FILE}" ]; then
    echo "❌ Error: File not found: ${PROCESS_FILE}"
    exit 1
fi

# Verify fix was applied (check for quoted labels)
QUOTED_COUNT=$(jq -r .mermaid "${PROCESS_FILE}" | grep -c '\["' 2>/dev/null || echo "0")
UNQUOTED_COLONS=$(jq -r .mermaid "${PROCESS_FILE}" | grep -cE '\[[^"]*:[^"]*\]' 2>/dev/null || echo "0")

if [ "${QUOTED_COUNT}" -eq 0 ]; then
    echo "⚠️  WARNING: No quoted labels found. Did you run the fix script?"
    echo "   Run: python3 scripts/fix_anaerobic_colons.py ${PROCESS_FILE}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if [ "${UNQUOTED_COLONS}" -gt 0 ]; then
    echo "⚠️  WARNING: ${UNQUOTED_COLONS} unquoted labels with colons still found!"
    echo "   Please run the fix script first."
    exit 1
fi

echo "✅ Verified: Fix appears to be applied (${QUOTED_COUNT} quoted labels found)"

# Upload to GCS
echo ""
echo "📤 Uploading to GCS..."
gsutil cp "${PROCESS_FILE}" "${GCS_PATH}"

# Set aggressive no-cache headers
echo "🔄 Setting cache-control headers (AGGRESSIVE - force refresh)..."
gsutil setmeta -h "Cache-Control:no-cache,no-store,must-revalidate" "${GCS_PATH}"
gsutil setmeta -h "Content-Type:application/json" "${GCS_PATH}"

# Verify upload
echo ""
echo "🔍 Verifying server copy..."
SERVER_QUOTED=$(curl -s "${GCS_PATH/https:\/\/storage.googleapis.com\//https://storage.googleapis.com/}" | jq -r .mermaid | grep -c '\["' 2>/dev/null || echo "0")

if [ "${SERVER_QUOTED}" -gt 0 ]; then
    echo "✅ Verified: Server copy has ${SERVER_QUOTED} quoted labels"
else
    echo "⚠️  Warning: Could not verify quoted labels on server"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🧪 Test URL (wait 2-3 minutes for propagation, then test in incognito):"
echo "   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration"
echo ""
echo "📋 What was fixed:"
echo "   • 5 labels wrapped in quotes (colons and (4Fe-4S)2+ patterns)"
echo "   • Should resolve Mermaid 10.6.1 parse error on line 12"

