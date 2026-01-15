#!/bin/bash

echo "=================================================="
echo "📋 UPLOADING SIMPLE TABLE VIEWER LAYOUT"
echo "=================================================="
echo ""
echo "This will upload the updated viewer with:"
echo "  • Simple HTML table (like database table)"
echo "  • Alphabetically sorted process list"
echo "  • 3 columns: Process Name | Organism | Category"
echo ""

# Pull latest changes
echo "Step 1: Pulling latest changes from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git checkout cursor/continue-frozen-deploy-glmp-conversation-0c90
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
echo "✅ Code updated!"
echo ""

# Upload viewer files
echo "Step 2: Uploading viewer files to GCS..."
gsutil -m cp \
  glmp-v2/viewer/index.html \
  glmp-v2/viewer/viewer.js \
  glmp-v2/viewer/styles.css \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/

echo ""
echo "Step 3: Setting cache control headers..."
gsutil -m setmeta -h "Cache-Control:no-cache, max-age=0" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/styles.css

echo ""
echo "=================================================="
echo "✅ SIMPLE TABLE VIEWER UPLOADED!"
echo "=================================================="
echo ""
echo "📋 Now view it at:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
echo "⚠️  IMPORTANT: Do a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)"
echo ""
echo "You should see:"
echo "  ✓ Simple table with 3 columns"
echo "  ✓ Alphabetically sorted processes"
echo "  ✓ Clean, compact layout (like database table)"
echo ""
