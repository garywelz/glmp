"""
Simple Process Suggestion Handler
Just captures and stores user suggestions - no AI chat
"""

import json
from datetime import datetime, timezone
from flask import Request
from google.cloud import storage

PROJECT_ID = "regal-scholar-453620-r7"
BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"

storage_client = storage.Client()


def glmp_simple_suggestion(request: Request):
    """HTTP Cloud Function to handle simple process suggestions"""
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        "Access-Control-Max-Age": "3600",
    }

    if request.method == "OPTIONS":
        return ("", 204, cors_headers)

    if request.method != "POST":
        return (json.dumps({"error": "POST only"}), 405, cors_headers)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return (json.dumps({"error": "Invalid JSON"}), 400, cors_headers)

    # Extract suggestion data
    suggestion_text = data.get("suggestion", "").strip()
    user_email = data.get("email", "").strip()  # Optional
    organism = data.get("organism", "").strip()  # Optional
    category = data.get("category", "").strip()  # Optional

    if not suggestion_text:
        return (json.dumps({"error": "Suggestion text is required"}), 400, cors_headers)

    # Create suggestion record
    suggestion = {
        "id": f"suggestion_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "suggestion": suggestion_text,
        "email": user_email,
        "organism": organism,
        "category": category,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending"
    }

    # Save to GCS
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Append to suggestions file (JSONL format - one JSON object per line)
        blob = bucket.blob("glmp-process-suggestions/suggestions.jsonl")
        
        # Read existing suggestions
        existing_content = ""
        try:
            if blob.exists():
                existing_content = blob.download_as_text()
        except Exception:
            pass  # File doesn't exist yet, start fresh
        
        # Append new suggestion
        new_line = json.dumps(suggestion, separators=(",", ":")) + "\n"
        new_content = existing_content + new_line
        
        # Upload updated content
        blob.upload_from_string(new_content, content_type="application/json")
        
        print(f"✓ Saved suggestion: {suggestion['id']}")
        
        return (json.dumps({
            "status": "success",
            "message": "Thank you! Your suggestion has been saved.",
            "suggestionId": suggestion["id"]
        }), 200, cors_headers)
        
    except Exception as e:
        print(f"Error saving suggestion: {e}")
        return (json.dumps({
            "error": "Failed to save suggestion",
            "details": str(e)
        }), 500, cors_headers)


