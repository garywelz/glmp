#!/bin/bash
# Deploy ALL files that have been fixed for syntax issues

BUCKET="gs://regal-scholar-453620-r7-podcast-storage"
BASE_DIR="processes_with_not_gates"

echo "🚀 Deploying all syntax-fixed files..."
echo ""

# Find all files with backup files (indicating they were fixed)
FIXED_FILES=($(find "$BASE_DIR" -name "*.json.backup*" -o -name "*.backup" | sed 's/\.backup.*$//' | sort -u | sed "s|^$BASE_DIR/||"))

if [ ${#FIXED_FILES[@]} -eq 0 ]; then
    echo "⚠️  No fixed files found (no backup files detected)"
    echo "   This might mean all fixes were applied without creating backups"
    echo ""
    echo "   Deploying all files from processes_with_not_gates instead..."
    FIXED_FILES=($(find "$BASE_DIR" -name "*.json" | sed "s|^$BASE_DIR/||" | sort))
fi

echo "📋 Found ${#FIXED_FILES[@]} files to deploy"
echo ""

COUNT=0
ERRORS=0

for file in "${FIXED_FILES[@]}"; do
    LOCAL_FILE="${BASE_DIR}/${file}"
    GCS_PATH="glmp-v2/processes/${file}"
    
    if [ -f "$LOCAL_FILE" ]; then
        COUNT=$((COUNT + 1))
        if [ $((COUNT % 10)) -eq 0 ]; then
            echo "[$COUNT/${#FIXED_FILES[@]}] Deploying..."
        fi
        
        gsutil -h "Cache-Control:no-cache, no-store, must-revalidate, max-age=0" \
            cp "$LOCAL_FILE" "${BUCKET}/${GCS_PATH}" > /dev/null 2>&1
        
        if [ $? -ne 0 ]; then
            ERRORS=$((ERRORS + 1))
            echo "❌ Failed: ${file##*/}"
        fi
    fi
done

echo ""
echo "✅ Deployment complete!"
echo "   Deployed: $COUNT files"
if [ $ERRORS -gt 0 ]; then
    echo "   Errors: $ERRORS files"
fi
echo ""
echo "🧪 Test a few files to verify:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_antibiotic_efflux_pumps"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_biofilm_formation"
