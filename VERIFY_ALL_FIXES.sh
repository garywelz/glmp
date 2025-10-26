#!/bin/bash

# GLMP Complete Verification Script
# Verifies:
# 1. Data fixes (NOT gate metadata sync)
# 2. Viewer UX improvements

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                      🔍 GLMP DEPLOYMENT VERIFICATION                         ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 PART 1: Verifying Data Fixes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Download and check metadata.json
echo "🔄 Fetching deployed metadata.json..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json?nocache=$(date +%s)" > /tmp/deployed_metadata.json

echo ""
python3 << 'PYCHECK'
import json

with open('/tmp/deployed_metadata.json') as f:
    metadata = json.load(f)

print("📊 METADATA STATISTICS:")
print("━" * 80)
stats = metadata.get('statistics', {})
print(f"  OR gates:        {stats.get('orGates', 'MISSING')}")
print(f"  AND gates:       {stats.get('andGates', 'MISSING')}")
print(f"  NOT gates:       {stats.get('notGates', 'MISSING')}")
print(f"  Total gates:     {stats.get('totalLogicGates', 'MISSING')}")
print(f"  Conditionals:    {stats.get('totalConditionals', 'MISSING')}")
print(f"  Total nodes:     {stats.get('totalNodes', 'MISSING')}")
print()

# Check specific processes that user reported
print("🔬 CHECKING SPECIFIC PROCESSES:")
print("━" * 80)

for proc in metadata['processes']:
    if proc['id'] == 'ecoli_amino_acid_biosynthesis':
        not_gates = proc.get('notGates', 'MISSING')
        logic_not = proc.get('logicGates', {}).get('not', 'MISSING')
        match = "✅" if not_gates == logic_not == 5 else "❌"
        print(f"{match} Amino Acid Biosynthesis:")
        print(f"     notGates: {not_gates}")
        print(f"     logicGates.not: {logic_not}")
        print(f"     Expected: 5")
        print()
    
    if proc['id'] == 'ecoli_anaerobic_respiration':
        not_gates = proc.get('notGates', 'MISSING')
        logic_not = proc.get('logicGates', {}).get('not', 'MISSING')
        match = "✅" if not_gates == logic_not == 7 else "❌"
        print(f"{match} Anaerobic Respiration:")
        print(f"     notGates: {not_gates}")
        print(f"     logicGates.not: {logic_not}")
        print(f"     Expected: 7")
        print()

# Overall validation
print("━" * 80)
print("🎯 VALIDATION RESULTS:")
print("━" * 80)

total_not = stats.get('notGates', 0)
total_nodes = stats.get('totalNodes', 0)
total_conditionals = stats.get('totalConditionals', 0)

if total_not == 470:
    print("✅ Total NOT gates: 470 (CORRECT!)")
else:
    print(f"❌ Total NOT gates: {total_not} (Expected: 470)")

if total_nodes == 7273:
    print("✅ Total nodes: 7,273 (CORRECT!)")
else:
    print(f"❌ Total nodes: {total_nodes} (Expected: 7,273)")

if total_conditionals == 6231:
    print("✅ Total conditionals: 6,231 (CORRECT!)")
else:
    print(f"❌ Total conditionals: {total_conditionals} (Expected: 6,231)")

print()

# Check field consistency
print("🔍 Checking notGates field consistency...")
mismatches = 0
for proc in metadata['processes']:
    not_gates = proc.get('notGates', 0)
    logic_not = proc.get('logicGates', {}).get('not', 0)
    if not_gates != logic_not:
        mismatches += 1
        if mismatches <= 5:
            print(f"❌ {proc['id']}: notGates={not_gates}, logicGates.not={logic_not}")

if mismatches == 0:
    print("✅ All 108 processes have consistent notGates fields!")
else:
    print(f"❌ Found {mismatches} processes with inconsistent notGates fields")

print()
PYCHECK

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 PART 2: Verifying Viewer UX"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check viewer.js for loading optimization
echo "🔄 Checking viewer.js for loading optimization..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js?nocache=$(date +%s)" > /tmp/deployed_viewer.js

if grep -q "Show process view with loading state IMMEDIATELY" /tmp/deployed_viewer.js; then
    echo "✅ Loading optimization found in viewer.js"
else
    echo "❌ Loading optimization NOT found in viewer.js"
fi

if grep -q "Loading process diagram..." /tmp/deployed_viewer.js; then
    echo "✅ Loading spinner message found"
else
    echo "❌ Loading spinner message NOT found"
fi

echo ""

# Check index.html for layout changes
echo "📄 Checking index.html for layout improvements..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?nocache=$(date +%s)" > /tmp/deployed_index.html

if grep -q "DIAGRAM FIRST" /tmp/deployed_index.html; then
    echo "✅ Diagram-first layout comment found"
else
    echo "❌ Diagram-first layout comment NOT found"
fi

if grep -q "expandable-section" /tmp/deployed_index.html; then
    echo "✅ Expandable sections found"
else
    echo "❌ Expandable sections NOT found"
fi

if grep -q "process-description-short" /tmp/deployed_index.html; then
    echo "✅ Compact description found"
else
    echo "❌ Compact description NOT found"
fi

echo ""

# Check styles.css for new styles
echo "🎨 Checking styles.css for new styles..."
curl -s "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/styles.css?nocache=$(date +%s)" > /tmp/deployed_styles.css

if grep -q "Expandable Sections" /tmp/deployed_styles.css; then
    echo "✅ Expandable section styles found"
else
    echo "❌ Expandable section styles NOT found"
fi

if grep -q "Compact Description" /tmp/deployed_styles.css; then
    echo "✅ Compact description styles found"
else
    echo "❌ Compact description styles NOT found"
fi

if grep -q "Diagram Container - Make it prominent" /tmp/deployed_styles.css; then
    echo "✅ Prominent diagram styles found"
else
    echo "❌ Prominent diagram styles NOT found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ VERIFICATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 NEXT STEPS:"
echo ""
echo "  1. Hard refresh database table: Ctrl+Shift+R"
echo "  2. Check NOT gate counts for Amino Acid (should be 5)"
echo "  3. Check NOT gate counts for Anaerobic Respiration (should be 7)"
echo "  4. Test viewer with a process link"
echo "  5. Verify diagram appears immediately at top"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup
rm -f /tmp/deployed_metadata.json /tmp/deployed_viewer.js /tmp/deployed_index.html /tmp/deployed_styles.css
