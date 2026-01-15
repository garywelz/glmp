"""
Comments Storage System for Process Feedback
Stores comments/suggestions directly associated with each process JSON
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from google.cloud import storage


def get_comments_file_path(process_id: str) -> str:
    """Get the GCS path for a process's comments file"""
    organism = process_id.split('_')[0]  # e.g., 'ecoli' from 'ecoli_lac_operon'
    return f"glmp-v2/comments/{organism}/{process_id}_comments.json"


def load_comments(process_id: str, bucket_name: str) -> List[Dict]:
    """Load comments for a process"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        file_path = get_comments_file_path(process_id)
        blob = bucket.blob(file_path)
        
        if blob.exists():
            content = blob.download_as_text()
            data = json.loads(content)
            return data.get("comments", [])
        return []
    except Exception as e:
        print(f"Error loading comments: {e}")
        return []


def save_comment(process_id: str, comment: Dict, bucket_name: str) -> bool:
    """
    Save a new comment to the process's comments file
    
    Comment structure:
    {
        "id": "unique_id",
        "processId": "ecoli_lac_operon",
        "author": "user@example.com" or "Anonymous",
        "role": "researcher" | "student" | "expert" | "other",
        "issueType": "typo" | "logic_error" | "missing_info" | "suggestion" | "question",
        "nodeOrEdge": "A1" or null,
        "suggestion": "text of suggestion",
        "rationale": "why this change is needed",
        "references": "optional citations",
        "status": "pending" | "applied" | "rejected" | "under_review",
        "llm_analysis": {...},  # from LLM analysis
        "createdAt": "ISO timestamp",
        "replies": [  # threaded replies
            {
                "id": "reply_id",
                "author": "admin@glmp.bio",
                "message": "Thank you! This has been applied.",
                "createdAt": "ISO timestamp"
            }
        ]
    }
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        file_path = get_comments_file_path(process_id)
        blob = bucket.blob(file_path)
        
        # Load existing comments
        existing_comments = load_comments(process_id, bucket_name)
        
        # Add new comment
        comment.setdefault("id", f"comment_{int(datetime.now(timezone.utc).timestamp())}")
        comment.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
        comment.setdefault("status", "pending")
        comment.setdefault("replies", [])
        comment["processId"] = process_id
        
        existing_comments.append(comment)
        
        # Save back
        comments_data = {
            "processId": process_id,
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
            "totalComments": len(existing_comments),
            "comments": existing_comments
        }
        
        blob.upload_from_string(
            json.dumps(comments_data, indent=2),
            content_type="application/json"
        )
        
        print(f"✓ Saved comment {comment['id']} for process {process_id}")
        return True
        
    except Exception as e:
        print(f"Error saving comment: {e}")
        return False


def add_reply_to_comment(process_id: str, comment_id: str, reply: Dict, bucket_name: str) -> bool:
    """Add a reply to an existing comment"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        file_path = get_comments_file_path(process_id)
        blob = bucket.blob(file_path)
        
        if not blob.exists():
            return False
        
        content = blob.download_as_text()
        data = json.loads(content)
        comments = data.get("comments", [])
        
        # Find comment and add reply
        for comment in comments:
            if comment.get("id") == comment_id:
                reply.setdefault("id", f"reply_{int(datetime.now(timezone.utc).timestamp())}")
                reply.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
                comment.setdefault("replies", []).append(reply)
                
                # Update metadata
                data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
                
                # Save back
                blob.upload_from_string(
                    json.dumps(data, indent=2),
                    content_type="application/json"
                )
                
                print(f"✓ Added reply to comment {comment_id}")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error adding reply: {e}")
        return False


def update_comment_status(process_id: str, comment_id: str, new_status: str, bucket_name: str) -> bool:
    """Update the status of a comment (e.g., 'pending' -> 'applied')"""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        file_path = get_comments_file_path(process_id)
        blob = bucket.blob(file_path)
        
        if not blob.exists():
            return False
        
        content = blob.download_as_text()
        data = json.loads(content)
        comments = data.get("comments", [])
        
        # Find and update comment
        for comment in comments:
            if comment.get("id") == comment_id:
                comment["status"] = new_status
                comment["statusUpdatedAt"] = datetime.now(timezone.utc).isoformat()
                
                # Update metadata
                data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
                
                # Save back
                blob.upload_from_string(
                    json.dumps(data, indent=2),
                    content_type="application/json"
                )
                
                print(f"✓ Updated comment {comment_id} status to {new_status}")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error updating comment status: {e}")
        return False



