# GLMP API Documentation

## Overview
GLMP uses Google Cloud Functions for backend services. All endpoints support CORS and return JSON responses.

## Base URLs
- **Production**: `https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/`

## Endpoints

### 1. Process Feedback (`glmp_feedback`)

**Endpoint**: `POST /glmp_feedback`

**Purpose**: Submit feedback, comments, or corrections about a process

**Request Body**:
```json
{
  "processId": "ecoli_lac_operon",
  "processName": "Lac Operon",
  "issueType": "error|suggestion|question",
  "nodeOrEdge": "A1",
  "suggestion": "Text of suggestion",
  "rationale": "Why this change is needed",
  "references": "PubMed IDs or citations",
  "email": "user@example.com",
  "role": "researcher|student|other"
}
```

**Response** (200):
```json
{
  "status": "success",
  "message": "Feedback received",
  "feedbackId": "feedback_1234567890"
}
```

**Additional Features**:
- **GET** `/glmp_feedback?processId=ecoli_lac_operon` - Retrieve comments for a process
- Automatically analyzes feedback with LLM
- Saves comments to process JSON files
- Logs to GCS: `glmp-feedback/feedback.jsonl`

---

### 2. Simple Process Suggestion (`glmp_simple_suggestion`)

**Endpoint**: `POST /glmp_simple_suggestion`

**Purpose**: Submit a simple suggestion for a new process to be analyzed

**Request Body**:
```json
{
  "suggestion": "E. coli Quorum Sensing",
  "organism": "E. coli",
  "category": "Signal Transduction",
  "email": "user@example.com"
}
```

**Required Fields**:
- `suggestion` (string) - Description of the process

**Optional Fields**:
- `organism` (string) - Organism name
- `category` (string) - Process category
- `email` (string) - User email for updates

**Response** (200):
```json
{
  "status": "success",
  "message": "Thank you! Your suggestion has been saved.",
  "suggestionId": "suggestion_1234567890"
}
```

**Storage**: Saves to `glmp-process-suggestions/suggestions.jsonl` (JSONL format)

---

### 3. View Suggestions (`glmp_view_suggestions`)

**Endpoint**: `GET /glmp_view_suggestions`

**Purpose**: Retrieve all submitted process suggestions

**Response** (200):
```json
{
  "suggestions": [
    {
      "id": "suggestion_1234567890",
      "suggestion": "E. coli Quorum Sensing",
      "email": "user@example.com",
      "organism": "E. coli",
      "category": "Signal Transduction",
      "timestamp": "2025-01-XXT12:00:00Z",
      "status": "pending"
    }
  ],
  "count": 1
}
```

**Notes**:
- Suggestions are sorted by timestamp (newest first)
- Returns empty array if no suggestions exist

---

### 4. Process Suggestion Chat (`glmp_process_suggestion`)

**Endpoint**: `POST /glmp_process_suggestion`

**Purpose**: AI-powered chat interface for process generation (currently unused)

**Status**: ⚠️ Complex system, replaced by simple suggestion form

**Note**: This endpoint exists but is not actively used. The simple suggestion system is preferred.

---

## CORS Configuration

All endpoints support CORS with the following headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With
Access-Control-Max-Age: 3600
```

## Error Responses

All endpoints return consistent error formats:

**400 Bad Request**:
```json
{
  "error": "Missing required fields"
}
```

**405 Method Not Allowed**:
```json
{
  "error": "POST only"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Failed to save suggestion",
  "details": "Error message"
}
```

## Data Storage

### Google Cloud Storage Structure
```
gs://regal-scholar-453620-r7-podcast-storage/
├── glmp-v2/
│   ├── processes/
│   │   ├── ecoli/
│   │   └── yeast/
│   └── metadata.json
├── glmp-feedback/
│   └── feedback.jsonl
└── glmp-process-suggestions/
    └── suggestions.jsonl
```

## Authentication

Currently, all endpoints are publicly accessible. No authentication required.

## Rate Limiting

No rate limiting currently implemented. Consider adding if abuse occurs.

## Monitoring

- Cloud Functions logs available in Google Cloud Console
- Feedback logged to `glmp-feedback/feedback.jsonl`
- Suggestions logged to `glmp-process-suggestions/suggestions.jsonl`



