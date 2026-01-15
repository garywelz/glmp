#!/bin/bash
# Verify deployment after upload

echo "🔍 VERIFICATION SCRIPT"
echo "=================================="
echo ""

echo "Downloading deployed metadata.json..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json?nocache=$(date +%s)" > /tmp/deployed_metadata.json

echo "Checking deployed metadata..."
python3 << 'PYCHECK'
import json

with open('/tmp/deployed_metadata.json') as f:
    metadata = json.load(f)

total_or = sum(p.get('logicGates', {}).get('or', 0) for p in metadata['processes'])
total_and = sum(p.get('logicGates', {}).get('and', 0) for p in metadata['processes'])
total_not = sum(p.get('logicGates', {}).get('not', 0) for p in metadata['processes'])

print(f"\n✅ DEPLOYED METADATA STATS:")
print(f"   OR gates:  {total_or}")
print(f"   AND gates: {total_and}")
print(f"   NOT gates: {total_not}")
print(f"   Total: {total_or + total_and + total_not}")
print()

if total_not == 470:
    print("✅ SUCCESS! NOT gates = 470")
elif total_not == 127:
    print("❌ OLD FILE! Still showing 127 NOT gates")
    print("   Metadata upload may have failed or cache issue")
elif total_not == 126:
    print("❌ VERY OLD FILE! Still showing 126 NOT gates")
    print("   Metadata upload definitely failed")
else:
    print(f"⚠️  UNEXPECTED: NOT gates = {total_not}")

PYCHECK

echo ""
echo "=================================="
