"""
View Process Suggestions
Simple endpoint to view stored suggestions
"""

import json
from flask import Request
from google.cloud import storage

PROJECT_ID = "regal-scholar-453620-r7"
BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"

storage_client = storage.Client()


def glmp_view_suggestions(request: Request):
    """HTTP Cloud Function to view stored suggestions"""
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        "Access-Control-Max-Age": "3600",
    }

    if request.method == "OPTIONS":
        return ("", 204, cors_headers)

    if request.method != "GET":
        return (json.dumps({"error": "GET only"}), 405, cors_headers)

    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob("glmp-process-suggestions/suggestions.jsonl")
        
        if not blob.exists():
            return (json.dumps({
                "suggestions": [],
                "count": 0,
                "message": "No suggestions yet"
            }), 200, cors_headers)
        
        content = blob.download_as_text()
        
        # Parse JSONL (one JSON object per line)
        suggestions = []
        for line in content.strip().split('\n'):
            if line.strip():
                try:
                    suggestion = json.loads(line)
                    suggestions.append(suggestion)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp (newest first)
        suggestions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return (json.dumps({
            "suggestions": suggestions,
            "count": len(suggestions)
        }, indent=2), 200, cors_headers)
        
    except Exception as e:
        return (json.dumps({
            "error": "Failed to load suggestions",
            "details": str(e)
        }), 500, cors_headers)


