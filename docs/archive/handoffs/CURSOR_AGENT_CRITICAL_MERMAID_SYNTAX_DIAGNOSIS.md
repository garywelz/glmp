# 🔴 CRITICAL: Persistent Mermaid Syntax Error - Deep Diagnostic Request

## Context
**File:** `ecoli_anaerobic_respiration.json`  
**Viewer URL:** https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration  
**Mermaid Version:** 10.6.1  
**Status:** ❌ Still shows "Syntax error in text" despite multiple fix attempts

## Fixes Already Applied (But Error Persists)
1. ✅ Brackets: `[4Fe-4S]` → `(4Fe-4S)` (chemistry notation)
2. ✅ Double curlies: `{{...}}` → `{...}` (diamond nodes)
3. ✅ Tildes: `ArcA~P` → `ArcA-P` (phosphorylation notation)
4. ✅ File deployed to GCS with no-cache headers
5. ✅ Verified: Server copy matches local file (all 3 fixes present)

## 🔴 CONFIRMED ROOT CAUSE: Colons in Node Labels (Quote-Wrapped Fix)

**Cursor.com Agent Confirmed:** Colons (`:`) inside node labels `[...]` break Mermaid 10.6.1 parsing.

**Exact Parser Error:**
```
Parse error on line 12:
...conditions: FNR has (4Fe-4S)2+ cluster]
-----------------------^
```

**Problematic Lines:**
- Line 12: `A8[Under aerobic conditions: FNR has (4Fe-4S)2+ cluster]`
- Line 56: `A38[High O2: quinones oxidized by cytochrome oxidases]`
- Line 57: `A39[Low O2: quinones accumulate in reduced form]`

**Why This Breaks:** Mermaid treats bare colons (`:`) inside bracketed node labels as syntax tokens. The parser stops at the colon, causing a parse error.

**Also Problematic:** Labels containing `(...)2+` patterns (like `(4Fe-4S)2+`) also trigger tokenization issues once colons are fixed.

**✅ CONFIRMED FIX:** Wrap problematic labels in **quotes**:
- `A8[Under aerobic conditions: FNR has (4Fe-4S)2+ cluster]` 
  → `A8["Under aerobic conditions: FNR has (4Fe-4S)2+ cluster"]`
- `A38[High O2: quinones oxidized by cytochrome oxidases]` 
  → `A38["High O2: quinones oxidized by cytochrome oxidases"]`
- `A39[Low O2: quinones accumulate in reduced form]` 
  → `A39["Low O2: quinones accumulate in reduced form"]`

**Fix Pattern:** Any node label containing:
- A colon (`:`) inside brackets
- OR a pattern like `(...)2+` (parentheses followed by number and plus)

Should be wrapped in quotes: `["label content"]` instead of `[label content]`

## Your Mission: Find the REAL Root Cause

The pattern-matching approach has failed. We need **actual Mermaid parser validation**.

### Required Diagnostic Steps:

#### 1. **Capture EXACT Parser Error from Browser Console**

**CRITICAL FIRST STEP:** The viewer shows "Syntax error in text" but we need the actual error details.

```bash
# Open browser DevTools Console and capture the exact error
# Expected format from Mermaid.js:
# "Error: Parse error on line X: Unexpected 'TOKEN'"
# "Syntax error in graph"
```

**How to capture:**
1. Open the viewer URL in browser (incognito mode)
2. Press F12 → Console tab
3. Look for red error messages from Mermaid
4. Copy the EXACT error message and line number

**Or test locally:**
```bash
# Extract Mermaid string
jq -r .mermaid processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json > /tmp/test.mmd

# Create test HTML to see console error
cat > /tmp/test_mermaid.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
</head>
<body>
  <div class="mermaid"></div>
  <script>
    mermaid.initialize({startOnLoad:false});
    const mermaidCode = `<PASTE_MERMAID_STRING_HERE>`;
    document.querySelector('.mermaid').textContent = mermaidCode;
    mermaid.init(undefined, '.mermaid').catch(err => {
      console.error('MERMAID ERROR:', err);
      alert('Error: ' + err.message);
    });
  </script>
</body>
</html>
EOF
# Then open /tmp/test_mermaid.html and check console
```

#### 2. **Verify Colons in Node Labels (PRIMARY SUSPECT)**

```bash
FILE="processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"

# Find ALL colons in node labels (inside square brackets)
jq -r .mermaid "$FILE" | grep -nE '\[[^\]]*:[^\]]*\]'

# Expected output showing problematic lines:
# 12: A8[Under aerobic conditions: FNR has (4Fe-4S)2+ cluster]
# 56: A38[High O2: quinones oxidized by cytochrome oxidases]
# 57: A39[Low O2: quinones accumulate in reduced form]
```

#### 3. **Check for Hidden Syntax Violations**
Run these checks and report findings:

```bash
FILE="processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"

# A) Check for unmatched brackets/parentheses
jq -r .mermaid "$FILE" | grep -oE '[\[\]{}()]' | sort | uniq -c

# B) Check edge label syntax (pipe notation |label|)
jq -r .mermaid "$FILE" | grep -nE '\|.*\|' | head -20

# C) Check for special characters that might need escaping
jq -r .mermaid "$FILE" | grep -nE '[<>#@$%^&*+=]' | head -20

# D) Check for Unicode/hidden characters
jq -r .mermaid "$FILE" | hexdump -C | grep -E '[^20-7e]'

# E) Check node ID syntax (must be alphanumeric, no spaces)
jq -r .mermaid "$FILE" | grep -oE '\b[A-Z][0-9]+\b' | sort | uniq -d

# F) Check for invalid node shape syntax
jq -r .mermaid "$FILE" | grep -nE '\[.*\[|\(.*\(|\{.*\{' | head -20
```

#### 4. **Compare with a WORKING Process**
Find a process that renders successfully and compare syntax patterns:

```bash
# Find a working process (check viewer manually)
WORKING="processes_with_not_gates/ecoli/ecoli_lac_operon.json"  # Example

# Compare node label patterns
echo "=== PROBLEMATIC FILE ==="
jq -r .mermaid "$FILE" | grep -oE '\[[^\]]+\]' | head -10

echo "=== WORKING FILE ==="
jq -r .mermaid "$WORKING" | grep -oE '\[[^\]]+\]' | head -10
```

#### 5. **Test Actual Mermaid Rendering (WITH ERROR CAPTURE)**
If possible, create a minimal test HTML file that renders ONLY this diagram:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
</head>
<body>
  <div class="mermaid"></div>
  <script>
    mermaid.initialize({startOnLoad:false, logLevel: 'error'});
    const mermaidCode = `<PASTE_EXACT_MERMAID_STRING_HERE>`;
    document.querySelector('.mermaid').textContent = mermaidCode;
    
    // Capture errors explicitly
    mermaid.init(undefined, '.mermaid').catch(err => {
      console.error('🔴 MERMAID PARSER ERROR:', err);
      console.error('Error message:', err.message);
      console.error('Error stack:', err.stack);
      document.body.innerHTML = '<h1>ERROR</h1><pre>' + err.message + '</pre>';
    });
  </script>
</body>
</html>
```

**Critical:** Open browser DevTools Console (F12) and capture:
- Exact error message
- Line number in Mermaid code
- Token that caused the failure

#### 6. **Fix Colons in Node Labels (QUOTE-WRAP FIX)**

**✅ CONFIRMED SOLUTION:** Wrap labels containing colons or `(...)2+` patterns in quotes.

**Quick Fix Script (Recommended):**
```bash
# Run the automated fix script
python3 scripts/fix_anaerobic_colons.py processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json
```

**Manual Method (Alternative):**
```bash
FILE="processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"

# Method 1: Use inline Python script
python3 << 'PYTHON_SCRIPT'
import json
import re

file_path = "processes_with_not_gates/ecoli/ecoli_anaerobic_respiration.json"
with open(file_path, 'r') as f:
    data = json.load(f)

mermaid = data['mermaid']

# Pattern: Find node definitions with labels containing colon OR (...)+ pattern
# Matches: A8[text: more text] or A10[text with (stuff)+ more]
# Replace with: A8["text: more text"]

def quote_problematic_labels(text):
    # Match: node_id[label with colon or (...)+ pattern]
    # Group 1: node_id (A8, A38, etc.)
    # Group 2: label content
    pattern = r'(\w+)\[([^\]]*(?::|\([^)]+\)\d+\+)[^\]]*)\]'
    
    def replacer(match):
        node_id = match.group(1)
        label = match.group(2)
        return f'{node_id}["{label}"]'
    
    return re.sub(pattern, replacer, text)

fixed_mermaid = quote_problematic_labels(mermaid)

# Verify fixes
print("=== BEFORE ===")
for line in mermaid.split('\n'):
    if re.search(r'\[[^\]]*:[^\]]*\]', line):
        print(line.strip())

print("\n=== AFTER ===")
for line in fixed_mermaid.split('\n'):
    if re.search(r'\["[^"]*:[^"]*"\]', line):
        print(line.strip())

# Save
data['mermaid'] = fixed_mermaid
with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

print("\n✅ Fixed file saved")
PYTHON_SCRIPT

# Method 2: Manual jq replacements (if Python unavailable)
# jq '.mermaid |= gsub("A8\\[Under aerobic conditions: FNR has \\(4Fe-4S\\)2\\+ cluster\\]"; "A8[\"Under aerobic conditions: FNR has (4Fe-4S)2+ cluster\"]")' "$FILE" > "${FILE}.fixed"
```

**Specific replacements needed:**
- `A8[Under aerobic conditions: FNR has (4Fe-4S)2+ cluster]` → `A8["Under aerobic conditions: FNR has (4Fe-4S)2+ cluster"]`
- `A38[High O2: quinones oxidized by cytochrome oxidases]` → `A38["High O2: quinones oxidized by cytochrome oxidases"]`
- `A39[Low O2: quinones accumulate in reduced form]` → `A39["Low O2: quinones accumulate in reduced form"]`
- Also check for any labels with `(...)2+` patterns and quote those too

#### 7. **Line-by-Line Syntax Check**
Extract and check specific problematic lines:

```bash
# Get specific lines that might be problematic
jq -r .mermaid "$FILE" | nl -ba | sed -n '45,80p'

# Focus on lines with:
# - Complex labels
# - Multiple special characters
# - Edge labels with hyphens or pipes
# - Subroutine nodes [/.../]
```

#### 8. **Check for Mermaid Version-Specific Issues**
Mermaid 10.6.1 might have specific syntax requirements. Check:
- Are there any deprecated syntax patterns?
- Are edge label pipes `|...|` properly formatted?
- Are node labels too long?
- Are there any conflicting style definitions?

## Expected Output

Please provide:
1. ✅ **Confirm the colon issue** - verify that colons in node labels are the root cause
2. ✅ **Browser console error message** - capture the exact Mermaid parser error from DevTools
3. ✅ **Fix for colons** - replace colons in node labels with appropriate alternative (semicolon, dash, or remove)
4. ✅ **Verification** - test in isolated HTML file with Mermaid 10.6.1 to confirm fix works
5. ✅ **Deployment script** - push the fixed file to GCS with no-cache headers
6. ✅ **Final verification** - confirm viewer renders without "Syntax error in text"

## Critical Constraints
- Only modify the `.mermaid` field (not metadata)
- Preserve all biological accuracy
- Keep node IDs unchanged
- Fix must work with Mermaid 10.6.1 (version used in viewer)

## Additional Context
The viewer is hosted on Google Cloud Storage and uses Mermaid.js 10.6.1 loaded via CDN. Cache has been aggressively cleared. Multiple browsers tested (incognito mode). Error persists across all tests, indicating it's a genuine syntax issue, not a caching problem.

---

**Priority:** 🔴 CRITICAL - This is blocking the viewer for one of the key processes.

**Estimated Complexity:** Medium-High (requires deep Mermaid parser knowledge)

**Time Estimate:** 30-60 minutes for thorough diagnosis

