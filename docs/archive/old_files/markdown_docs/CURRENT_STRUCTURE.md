# Current GLMP Structure

## Main Page (Hugging Face / index.html)

**Location:** `index.html` (root)
**URL:** `huggingface.co/spaces/garywelz/glmp` or GCS `index.html`

**Structure:**
- Header with title: "🧬 Genome Logic Modeling Project - Interactive Database Analysis"
- About button in header
- **Frame** containing: `glmp-database-table.html` (the rich database table with stats)

## Viewer (GCS)

**Location:** `glmp-v2/viewer/index.html`
**URL:** `storage.googleapis.com/.../glmp-v2/viewer/index.html`

**Structure:**
- **NO header** (since it's in a frame)
- **Simple process table** (Process Name, Organism, Category)
- When clicking a process → shows flowchart
- **Back button** on process view → returns to database table

## Database Table (GCS)

**Location:** `glmp-database-table.html`
**URL:** `storage.googleapis.com/.../glmp-database-table.html`

**Structure:**
- Rich table with statistics
- All 108 processes
- Logic gates, nodes, conditionals
- Click process name → opens flowchart (in viewer or new page)

## Navigation Flow

1. **User visits Hugging Face** → sees main page with database table in frame
2. **User clicks process in database table** → opens flowchart (viewer)
3. **User clicks "Back to GLMP Database Table"** → returns to database table
4. **User can also access viewer directly** → sees simple table, can click processes

## Files Deployed

### Main Page
- `index.html` → Shows frame with database table

### Viewer
- `glmp-v2/viewer/index.html` → Simple table view
- `glmp-v2/viewer/viewer.js` → Modularized (250 lines)
- `glmp-v2/viewer/modules/*.js` → 8 modules
- `glmp-v2/viewer/styles.css` → Styling
- `glmp-v2/viewer/metadata.json` → Local copy

### Database Table
- `glmp-database-table.html` → Rich table with stats



