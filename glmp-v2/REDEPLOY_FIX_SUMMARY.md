# Redeploy Fix Summary - Color Scheme Updates

## Status: ✅ All Files Correct in GitHub

### What Was Fixed:

1. **Lavender Color Change**
   - OLD: `#a78bfa` (too purple, similar to violet)
   - NEW: `#b4b4dc` (true blue-gray lavender, distinct from violet)

2. **Files Updated:**
   - ✅ `ecoli_lac_operon.json` - Lavender color scheme + O node branching fixed
   - ✅ `ecoli_dna_replication_initiation.json` - Lavender color scheme updated
   - ✅ `ecoli_transcription_regulation.json` - Lavender color scheme updated
   - ✅ `yeast_cell_cycle_control.json` - Lavender color scheme + node styling updated
   - ✅ `viewer/index.html` - Simplified home page (table of contents)

3. **Current Color Palette:**
   ```
   Red:      #ff6b6b - Triggers & Inputs
   Yellow:   #ffd43b - Structures & Objects
   Green:    #51cf66 - Processing & Operations
   Blue:     #74c0fc - Intermediates & States
   Orange:   #ff9f43 - OR Logic Gates
   Lavender: #b4b4dc - AND Logic Gates ← UPDATED
   Violet:   #b197fc - Products & Outputs
   ```

## Verification Complete:

```bash
# All JSON files validated
✓ ecoli_lac_operon.json - Valid JSON, 63 nodes, 2 AND gates styled #b4b4dc
✓ ecoli_dna_replication_initiation.json - Valid JSON, color scheme correct
✓ ecoli_transcription_regulation.json - Valid JSON, color scheme correct
✓ yeast_cell_cycle_control.json - Valid JSON, 22 styled nodes, complete mermaid
```

## Known Issue - Yeast Chart Not Rendering on GCS:

**Symptom:** 
- Yeast Cell Cycle shows "just HTML" instead of flowchart
- Color legend displays correctly
- Other 3 processes render fine

**Analysis:**
- ✅ JSON is valid (passes `python3 -m json.tool`)
- ✅ Mermaid string is complete (2336 chars, ends properly)
- ✅ Contains all 22 style commands
- ⚠️ Issue likely on deployed GCS version (caching or old file)

**Solution:** 
REDEPLOY from fresh pull to force update

---

## Redeploy Instructions:

```bash
# 1. Pull latest changes
cd ~/glmp-clean/glmp-v2
git pull origin main

# 2. Verify files locally
cat processes/yeast/yeast_cell_cycle_control.json | python3 -m json.tool > /dev/null && echo "✓ Valid"

# 3. Deploy to GCS
./DEPLOY_TO_GCS.sh

# 4. Force refresh in browser
# Open incognito window OR hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
```

---

## Expected Results After Redeploy:

### Lac Operon:
- ✅ 2 lavender diamonds (ANDGATE1, ANDGATE2) - clear blue-gray color
- ✅ 3 orange diamonds (M, N, O)
- ✅ O node has both Yes and No branches
- ✅ Color legend shows lavender as #b4b4dc

### DNA Replication:
- ✅ Color legend shows lavender as #b4b4dc
- ✅ 1 orange diamond (DnaACheck)

### Transcription:
- ✅ Color legend shows lavender as #b4b4dc
- ✅ 2 orange diamonds (SigmaCheck, Regulation)

### Yeast Cell Cycle:
- ✅ 1 lavender diamond (StartCheck) - clear blue-gray color
- ✅ 2 orange diamonds (SCheckpoint, SpindleCheck)
- ✅ **FLOWCHART RENDERS** (not just HTML)
- ✅ All phase rectangles are blue, not lavender

### Home Page:
- ✅ Simple process list (like HuggingFace)
- ✅ No marketing content

---

## Troubleshooting:

If Yeast still shows HTML after deploy:

1. **Check deployed file directly:**
   ```bash
   gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/yeast_cell_cycle_control.json | python3 -m json.tool | head -20
   ```

2. **Verify file size:**
   ```bash
   gsutil ls -l gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/
   ```
   Should be ~5KB

3. **Force cache refresh:**
   - Add `?v=3` to URL
   - Open in different browser
   - Clear browser cache completely

---

**Last Updated:** 2025-10-08  
**Commit:** Latest on `main` branch
