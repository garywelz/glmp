#!/bin/bash
# Deploy corrected metadata.json to GCS
# Run this from your local machine where gsutil is available

echo "🚀 Deploying Corrected Metadata to GCS"
echo "========================================"
echo ""

# Check if metadata file exists
if [ ! -f "metadata_recalculated.json" ]; then
    echo "❌ Error: metadata_recalculated.json not found"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

echo "📤 Uploading corrected metadata.json..."
gsutil cp metadata_recalculated.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json

if [ $? -eq 0 ]; then
    echo "✅ Upload successful"
else
    echo "❌ Upload failed"
    exit 1
fi

echo ""
echo "🔧 Setting cache-control headers..."
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" \
    gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json

if [ $? -eq 0 ]; then
    echo "✅ Headers set successfully"
else
    echo "⚠️  Warning: Failed to set headers"
fi

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "New Statistics:"
echo "  OR gates:  347"
echo "  AND gates: 444"
echo "  NOT gates: 127"
echo "  Conditionals: 5897"
echo ""
echo "Pattern: 347:444:127:5897"
echo ""
echo "The database table and viewer will now show corrected counts."
echo "Users can verify by counting colored nodes in flowcharts."
echo ""
