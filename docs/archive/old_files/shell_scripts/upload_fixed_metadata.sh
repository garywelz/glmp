#!/bin/bash
# Upload corrected metadata.json with all 100 processes

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING FIXED METADATA (100 processes)"
echo "=========================================="
echo ""

# Get the fixed metadata from GitHub
echo "Step 1: Fetching corrected metadata from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:metadata_100_complete.json > v2-development/data/metadata.json

echo "✅ Downloaded corrected metadata"
echo ""

# Show what we're uploading
echo "Step 2: Verifying metadata..."
python3 << 'PYTHON'
import json
with open('v2-development/data/metadata.json', 'r') as f:
    data = json.load(f)
    print(f"  Total processes: {data['totalProcesses']}")
    print(f"  Processes in array: {len(data['processes'])}")
    print(f"  E. coli: {data['organisms'][0]['processCount']}")
    print(f"  S. cerevisiae: {data['organisms'][1]['processCount']}")
    print(f"  B. subtilis: {data['organisms'][2]['processCount']}")
    print(f"  Total gates: {data['statistics']['totalLogicGates']}")
    print(f"  OR gates: {data['statistics']['orGates']}")
    print(f"  AND gates: {data['statistics']['andGates']}")
PYTHON

echo ""
echo "Step 3: Uploading to GCS..."
gsutil cp v2-development/data/metadata.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "Step 4: Setting cache headers to force refresh..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "✅ METADATA FIXED AND UPLOADED!"
echo "=========================================="
echo ""
echo "The viewer should now show all 100 processes!"
echo ""
echo "Refresh the viewer with a HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R"
echo "  • Mac: Cmd + Shift + R"
echo ""
echo "Viewer URL:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
echo ""
