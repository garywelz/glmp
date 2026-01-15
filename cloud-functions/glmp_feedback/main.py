import json
from datetime import datetime, timezone
from flask import make_response, Request

from google.cloud import storage
from feedback_processor import (
    analyze_feedback_with_llm,
    assess_risk_simple,
    apply_low_risk_change,
    save_process_update,
    add_to_review_queue
)
from comments_storage import save_comment, load_comments

# Configure your bucket and object path for JSONL feedback log
BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"
OBJECT_NAME = "glmp-feedback/feedback.jsonl"

storage_client = storage.Client()


def glmp_feedback(request: Request):
    """HTTP Cloud Function to receive GLMP feedback and append to JSONL in GCS."""
    # CORS headers - must be set for all responses
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        "Access-Control-Max-Age": "3600",
    }

    # Handle preflight OPTIONS request FIRST - use tuple format for Gen2
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Handle GET request for comments
    if request.method == "GET":
        process_id = request.args.get("processId", "")
        if process_id:
            try:
                comments = load_comments(process_id, BUCKET_NAME)
                return (json.dumps({"comments": comments}), 200, cors_headers)
            except Exception as e:
                return (json.dumps({"error": str(e)}), 500, cors_headers)
        return (json.dumps({"error": "processId required"}), 400, cors_headers)
    
    if request.method != "POST":
        return (json.dumps({"error": "POST only"}), 405, cors_headers)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        return (json.dumps({"error": "Invalid JSON"}), 400, cors_headers)

    # Minimal validation
    if not data.get("issueType") or not data.get("suggestion"):
        return (json.dumps({"error": "Missing required fields"}), 400, cors_headers)

    # Enrich with server-side metadata
    now = datetime.now(timezone.utc).isoformat()
    data["receivedAt"] = now
    data.setdefault("processId", "unknown")
    data.setdefault("processName", "unknown")

    # Log to Cloud Logging for debugging / audit
    print("GLMP_FEEDBACK", json.dumps(data))

    # Append one JSON object per line to a JSONL blob in GCS
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(OBJECT_NAME)

        try:
            existing = blob.download_as_text()
        except Exception:
            existing = ""

        line = json.dumps(data, separators=(",", ":")) + "\n"
        new_content = existing + line
        blob.upload_from_string(new_content, content_type="application/json")
    except Exception as e:
        print("Error writing feedback to GCS:", repr(e))
        return (json.dumps({"error": "Storage error"}), 500, cors_headers)

    # Save as comment immediately (non-blocking)
    try:
        comment_data = {
            "author": data.get("email", "Anonymous"),
            "role": data.get("role", "other"),
            "issueType": data.get("issueType", ""),
            "nodeOrEdge": data.get("nodeOrEdge", ""),
            "suggestion": data.get("suggestion", ""),
            "rationale": data.get("rationale", ""),
            "references": data.get("references", ""),
            "status": "pending"
        }
        save_comment(data.get("processId", "unknown"), comment_data, BUCKET_NAME)
    except Exception as e:
        print(f"Error saving comment (non-blocking): {e}")
    
    # Process feedback with LLM (async - don't block response)
    try:
        process_feedback_with_llm(data, BUCKET_NAME)
    except Exception as e:
        print(f"Error in LLM processing (non-blocking): {e}")
        # Continue - don't fail the request if LLM processing fails

    # Success response with CORS headers - use tuple format
    return (json.dumps({"status": "ok", "message": "Feedback saved as comment"}), 200, cors_headers)


def process_feedback_with_llm(feedback_data: dict, bucket_name: str):
    """
    Process feedback using LLM analysis (runs asynchronously)
    """
    print(f"🤖 Starting LLM analysis for feedback: {feedback_data.get('processId')}")
    
    # Load process data if available
    process_data = None
    process_id = feedback_data.get("processId", "")
    if process_id and process_id != "unknown":
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            organism = process_id.split('_')[0]
            file_path = f"glmp-v2/processes/{organism}/{process_id}.json"
            blob = bucket.blob(file_path)
            if blob.exists():
                process_data = json.loads(blob.download_as_text())
                print(f"✓ Loaded process data for {process_id}")
        except Exception as e:
            print(f"Could not load process data: {e}")
    
    # Analyze with LLM
    analysis = analyze_feedback_with_llm(feedback_data, process_data)
    print(f"📊 LLM Analysis: risk={analysis['risk_level']}, auto_apply={analysis['auto_apply']}, confidence={analysis['confidence']}")
    
    # Store analysis with feedback
    feedback_data["llm_analysis"] = analysis
    feedback_data["analyzed_at"] = datetime.now(timezone.utc).isoformat()
    
    # Update feedback log with analysis
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(OBJECT_NAME)
        
        # Re-read to append analyzed version
        try:
            existing = blob.download_as_text()
        except Exception:
            existing = ""
        
        analyzed_line = json.dumps(feedback_data, separators=(",", ":")) + "\n"
        new_content = existing + analyzed_line
        blob.upload_from_string(new_content, content_type="application/json")
    except Exception as e:
        print(f"Error updating feedback log: {e}")
    
    # Update comment with LLM analysis
    try:
        # Find the most recent comment for this feedback (by matching suggestion text)
        comments = load_comments(process_id, bucket_name)
        suggestion_text = feedback_data.get("suggestion", "")
        
        # Find matching comment (most recent with matching suggestion)
        matching_comment = None
        for comment in reversed(comments):
            if comment.get("suggestion") == suggestion_text and comment.get("status") == "pending":
                matching_comment = comment
                break
        
        if matching_comment:
            # Update comment with LLM analysis
            matching_comment["llm_analysis"] = analysis
            matching_comment["analyzed_at"] = datetime.now(timezone.utc).isoformat()
            
            # Update status based on analysis
            if analysis["auto_apply"] and analysis["risk_level"] == "low" and analysis["confidence"] > 0.7:
                matching_comment["status"] = "under_review"  # Will be "applied" after successful change
            elif analysis["risk_level"] == "high":
                matching_comment["status"] = "under_review"
            
            # Save updated comment
            from comments_storage import save_comment
            # Re-save the comment (we'll need to update the whole file)
            # For now, we'll handle this in the auto-apply section
    except Exception as e:
        print(f"Error updating comment with analysis: {e}")
    
    # Handle based on risk level
    if analysis["auto_apply"] and analysis["risk_level"] == "low" and analysis["confidence"] > 0.7:
        # Auto-apply low-risk changes
        print(f"✅ Auto-applying low-risk change")
        if process_data:
            success, message = apply_low_risk_change(
                process_data,
                analysis["suggested_changes"],
                feedback_data
            )
            if success:
                save_process_update(process_id, process_data, bucket_name)
                print(f"✓ Applied change: {message}")
                
                # Update comment status to "applied" and add reply
                try:
                    from comments_storage import update_comment_status, add_reply_to_comment
                    comments = load_comments(process_id, bucket_name)
                    suggestion_text = feedback_data.get("suggestion", "")
                    # Find the most recent matching comment
                    for comment in reversed(comments):
                        if comment.get("suggestion") == suggestion_text and comment.get("status") == "pending":
                            update_comment_status(process_id, comment["id"], "applied", bucket_name)
                            add_reply_to_comment(process_id, comment["id"], {
                                "author": "GLMP System",
                                "message": f"✅ Applied automatically: {message}"
                            }, bucket_name)
                            break
                except Exception as e:
                    print(f"Error updating comment after auto-apply: {e}")
            else:
                print(f"⚠️ Could not apply change: {message}")
                add_to_review_queue(feedback_data, analysis, bucket_name)
        else:
            print("⚠️ No process data available for auto-apply")
            add_to_review_queue(feedback_data, analysis, bucket_name)
    else:
        # Add to review queue
        print(f"📋 Adding to review queue (risk: {analysis['risk_level']})")
        add_to_review_queue(feedback_data, analysis, bucket_name)


# Email sending removed - using comments system instead


