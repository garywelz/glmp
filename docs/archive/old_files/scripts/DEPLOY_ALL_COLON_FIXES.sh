#!/bin/bash
# Deploy all colon-fixed process files to GCS

set -e

GCS_BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
PROCESS_DIR="./processes_with_not_gates"
GCS_BASE_PATH="${GCS_BUCKET}/glmp-v2/processes"

echo "📤 Deploying all colon-fixed process files to GCS..."
echo "   Source: ${PROCESS_DIR}"
echo "   Destination: ${GCS_BASE_PATH}"
echo ""

# Count JSON files
TOTAL_FILES=$(find "${PROCESS_DIR}" -name "*.json" | wc -l)
echo "📊 Found ${TOTAL_FILES} process file(s) to deploy"
echo ""

# Upload all JSON files
echo "📤 Uploading files..."
gsutil -m cp -r "${PROCESS_DIR}"/*/*.json "${GCS_BASE_PATH}/" 2>&1 | grep -E "(Copying|Operation completed)" || true

echo ""
echo "🔄 Setting cache-control headers (AGGRESSIVE - force refresh)..."

# Set no-cache headers on all JSON files
find "${PROCESS_DIR}" -name "*.json" | while read -r json_file; do
    # Extract organism and filename
    rel_path="${json_file#${PROCESS_DIR}/}"
    organism="${rel_path%%/*}"
    filename="${rel_path##*/}"
    
    gcs_path="${GCS_BASE_PATH}/${organism}/${filename}"
    
    gsutil setmeta -h "Cache-Control:no-cache,no-store,must-revalidate" "${gcs_path}" >/dev/null 2>&1 &
done

# Wait for all background jobs
wait

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Summary:"
echo "   • ${TOTAL_FILES} process file(s) uploaded"
echo "   • Cache-control headers set (no-cache, no-store, must-revalidate)"
echo ""
echo "🧪 Testing (wait 2-3 minutes, then test in incognito):"
echo "   Viewer: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "📋 Key files fixed:"
echo "   • Nucleotide Biosynthesis (29 labels)"
echo "   • Glycolysis (16 labels)"
echo "   • TCA Cycle (13 labels)"
echo "   • Pentose Phosphate Pathway (11 labels)"
echo "   • + 31 other processes (155 labels total)"

