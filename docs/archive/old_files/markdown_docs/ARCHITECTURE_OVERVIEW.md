# GLMP Architecture Overview

## System Components

### Frontend (Static Hosting - GCS)
**Location**: `glmp-v2/viewer/`

#### Core Files
- **index.html** - Main viewer page with process selector
- **viewer.js** (1,365 lines) - Core viewer logic
  - Process loading from GCS
  - Mermaid diagram rendering
  - Feedback submission
  - Navigation between processes
- **styles.css** - Styling for viewer

#### Additional Pages
- **simple-suggestion.html** - Simple process suggestion form
- **view-suggestions.html** - View submitted suggestions
- **process-suggestion-chat.html** - AI chat interface (unused)

**Hosting**: Google Cloud Storage (public bucket)
**URL**: `https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/`

---

### Backend (Google Cloud Functions)

#### 1. `glmp_feedback` (Active)
**Purpose**: Handle feedback, comments, and corrections
**Features**:
- LLM-powered feedback analysis
- Automatic risk assessment
- Comment storage in process JSONs
- Feedback logging to JSONL

**Files**:
- `main.py` - Entry point
- `feedback_processor.py` - LLM integration
- `comments_storage.py` - Comment management

**Endpoints**:
- `POST /glmp_feedback` - Submit feedback
- `GET /glmp_feedback?processId=X` - Get comments

#### 2. `glmp_simple_suggestion` (Active)
**Purpose**: Simple suggestion box for new processes
**Features**:
- Stores suggestions in JSONL format
- No AI processing (simple storage)

**Files**:
- `main.py` - Single file implementation

**Endpoints**:
- `POST /glmp_simple_suggestion` - Submit suggestion

#### 3. `glmp_view_suggestions` (Active)
**Purpose**: View stored suggestions
**Features**:
- Reads from JSONL file
- Returns sorted list (newest first)

**Files**:
- `main.py` - Single file implementation

**Endpoints**:
- `GET /glmp_view_suggestions` - Get all suggestions

#### 4. `glmp_process_suggestion` (Unused)
**Purpose**: AI-powered process generation chat
**Status**: ⚠️ Complex system, replaced by simple suggestion
**Recommendation**: Archive or remove

---

### Data Storage (Google Cloud Storage)

#### Structure
```
gs://regal-scholar-453620-r7-podcast-storage/
├── glmp-v2/
│   ├── processes/
│   │   ├── ecoli/
│   │   │   ├── ecoli_lac_operon.json
│   │   │   └── ...
│   │   └── yeast/
│   │       └── ...
│   ├── metadata.json
│   └── viewer/
│       ├── index.html
│       ├── viewer.js
│       └── styles.css
├── glmp-feedback/
│   └── feedback.jsonl
└── glmp-process-suggestions/
    └── suggestions.jsonl
```

#### Process JSON Schema
```json
{
  "id": "ecoli_lac_operon",
  "name": "Lac Operon",
  "organism": "E. coli",
  "category": "Gene Regulation",
  "description": "...",
  "mermaid": "graph TD\n...",
  "sources": [...],
  "comments": [...],
  "colorScheme": {...}
}
```

---

### Utilities (Scripts)

#### Active Scripts
- **validate_collection.py** - Validate all processes for errors
- **fix_mermaid_syntax.py** - Fix common Mermaid syntax issues

#### Archived Scripts
- Many one-time fix scripts (moved to archive)

---

## Data Flow

### Process Viewing
1. User opens viewer → Loads `metadata.json`
2. User selects process → Fetches process JSON from GCS
3. Viewer renders Mermaid diagram
4. User can submit feedback → Sent to `glmp_feedback`

### Feedback Submission
1. User submits feedback → `POST /glmp_feedback`
2. Function analyzes with LLM → Risk assessment
3. Low-risk changes applied automatically
4. High-risk changes queued for review
5. Comment saved to process JSON

### Process Suggestion
1. User submits suggestion → `POST /glmp_simple_suggestion`
2. Suggestion saved to JSONL file
3. Admin can view via `GET /glmp_view_suggestions`

---

## Technology Stack

### Frontend
- **HTML/CSS/JavaScript** (vanilla, no framework)
- **Mermaid.js** (v10.6.1) - Diagram rendering
- **Fetch API** - HTTP requests

### Backend
- **Python 3.9+**
- **Google Cloud Functions** (Gen 2)
- **Flask** - Request handling
- **Vertex AI Gemini** - LLM integration
- **Google Cloud Storage** - Data storage

### Infrastructure
- **Google Cloud Platform**
  - Cloud Functions
  - Cloud Storage
  - Vertex AI

---

## Security Considerations

### Current State
- All endpoints are publicly accessible
- No authentication required
- CORS enabled for all origins

### Recommendations
1. Add rate limiting to prevent abuse
2. Consider authentication for admin functions
3. Validate and sanitize all user inputs
4. Add request logging for audit trail

---

## Performance

### Current Optimizations
- Static file hosting (GCS) - Fast CDN delivery
- JSONL format for logs - Efficient appending
- Client-side rendering - Reduces server load

### Potential Improvements
1. Add caching headers for process JSONs
2. Implement CDN caching for static assets
3. Add compression for JSON responses
4. Consider pagination for large suggestion lists

---

## Known Issues

### Critical
1. **ecoli_stringent_response.json** - Mermaid syntax error (unfixable)
   - Status: Multiple fix attempts failed
   - Recommendation: Delete or regenerate

### Minor
1. **viewer.js** - Large monolithic file (1,365 lines)
   - Recommendation: Split into modules
2. **No error logging service** - Errors only in console
   - Recommendation: Add Cloud Logging integration

---

## Deployment

### Frontend
```bash
gsutil cp glmp-v2/viewer/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
```

### Backend
```bash
cd cloud-functions/glmp_feedback
./deploy.sh
```

### Process Updates
```bash
gsutil cp processes/ecoli/ecoli_lac_operon.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/
```

---

## Future Enhancements

1. **Process Generation** - Automate process creation from suggestions
2. **User Accounts** - Track contributions and reputation
3. **Version Control** - Track changes to processes over time
4. **Export Features** - PDF/SVG export of diagrams
5. **Search Functionality** - Full-text search across processes



