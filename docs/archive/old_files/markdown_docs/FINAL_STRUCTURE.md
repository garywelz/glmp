# Final GLMP Structure - Clarified

## Correct Structure

### 1. Main Page (Hugging Face / index.html)
**Location:** `index.html` (root, deployed to GCS)
**URL:** `huggingface.co/spaces/garywelz/glmp` or GCS `index.html`

**Contains:**
- Header with title: "🧬 Genome Logic Modeling Project - Interactive Database Analysis"
- About button in header
- **Frame** that loads: `glmp-database-table.html`

### 2. Database Table (GCS)
**Location:** `glmp-database-table.html`
**URL:** `storage.googleapis.com/.../glmp-database-table.html`

**Contains:**
- Rich database table with statistics
- All 108 processes listed
- **Each process name links to:** `glmp-v2/viewer/index.html?process=PROCESS_ID`

### 3. Process Pages (Viewer with ?process= parameter)
**Location:** `glmp-v2/viewer/index.html?process=PROCESS_ID`
**URL:** `storage.googleapis.com/.../glmp-v2/viewer/index.html?process=ecoli_lac_operon`

**Contains:**
- **Back button** at top: "← Back to GLMP Database Table"
- Process flowchart (loaded from JSON)
- Process details, feedback form, etc.

**How it works:**
1. Database table links to viewer with `?process=PROCESS_ID`
2. Viewer loads JSON from: `glmp-v2/processes/ORGANISM/PROCESS_ID.json`
3. Viewer displays the flowchart
4. Back button returns to database table

## What We Deployed

✅ **viewer.js** - With back button functionality
✅ **index.html** - Viewer page (only used with ?process= parameter)
✅ **All modules** - For rendering processes
✅ **Back button** - Appears on every process page

## Navigation Flow

1. User visits Hugging Face → sees main page with database table in frame
2. User clicks process in database table → opens `viewer/index.html?process=ID`
3. Viewer loads JSON and displays flowchart
4. **Back button appears at top** → returns to database table
5. User clicks back → returns to database table

## Important Notes

- **NO separate viewer index page needed** - viewer is only accessed via `?process=` parameter
- **Back button is on process pages** (when JSON is loaded and displayed)
- **Main page structure is correct** - frame contains database table



