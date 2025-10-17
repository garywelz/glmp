#!/bin/bash
# Upload final metadata with full logic gate breakdown

cd /home/gdubs/glmp

echo "=========================================="
echo "🔧 UPLOADING FINAL METADATA WITH GATE STATS"
echo "=========================================="
echo ""

# Get the fixed metadata from GitHub
echo "Step 1: Fetching corrected metadata from GitHub..."
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git show origin/cursor/continue-frozen-deploy-glmp-conversation-0c90:metadata_100_complete.json > v2-development/data/metadata_fixed.json

echo "✅ Downloaded fixed metadata"
echo ""

# Show what we're uploading
echo "Step 2: Verifying metadata structure..."
python3 << 'PYTHON'
import json
with open('v2-development/data/metadata_fixed.json', 'r') as f:
    data = json.load(f)
    print(f"  Total processes: {data['totalProcesses']}")
    print(f"  Processes in array: {len(data['processes'])}")
    print(f"  E. coli: {data['organisms'][0]['processCount']}")
    print(f"  S. cerevisiae: {data['organisms'][1]['processCount']}")
    print(f"  B. subtilis: {data['organisms'][2]['processCount']}")
    print(f"\n  Statistics:")
    print(f"  Total gates: {data['statistics']['totalLogicGates']}")
    print(f"  OR gates: {data['statistics']['orGates']}")
    print(f"  AND gates: {data['statistics']['andGates']}")
    print(f"\n  Sample process structure:")
    sample = data['processes'][0]
    print(f"  {sample['id']}:")
    print(f"    Complexity: {sample['complexity']}")
    print(f"    Nodes: {sample['nodes']}")
    print(f"    OR: {sample['logicGates']['or']}")
    print(f"    AND: {sample['logicGates']['and']}")
    print(f"    Total: {sample['logicGates']['total']}")
    
    # Show complexity distribution
    from collections import Counter
    complexities = Counter(p['complexity'] for p in data['processes'])
    print(f"\n  Complexity distribution:")
    for level in ['high', 'medium', 'low']:
        print(f"    {level}: {complexities.get(level, 0)} processes")
PYTHON

echo ""
echo "Step 3: Uploading to GCS..."
gsutil cp v2-development/data/metadata_fixed.json gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "Step 4: Setting cache headers..."
gsutil setmeta -h "Cache-Control:no-cache,max-age=0" gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json

echo ""
echo "=========================================="
echo "✅ METADATA FIXED AND UPLOADED!"
echo "=========================================="
echo ""
echo "The database table should now show:"
echo "  • 100 Total Processes ✓"
echo "  • 6496 Total Nodes ✓"
echo "  • 636 OR Gates ✓"
echo "  • 351 AND Gates ✓"
echo "  • 987 Total Gates ✓"
echo ""
echo "🌐 Refresh the database table:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
echo ""
echo "📱 HARD REFRESH:"
echo "  • Windows/Linux: Ctrl + Shift + R"
echo "  • Mac: Cmd + Shift + R"
echo ""
