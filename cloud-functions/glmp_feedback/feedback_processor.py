"""
Feedback Processor with LLM Integration
Analyzes feedback, determines risk level, and handles auto-apply or review queue
"""

import json
import re
from typing import Dict, Tuple, Optional
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = "regal-scholar-453620-r7"
REGION = "us-central1"

# Initialize Vertex AI (lazy - only when needed)
_gemini_model = None

def get_gemini_model():
    """Get or initialize Gemini model (lazy initialization with fallback)"""
    global _gemini_model
    if _gemini_model is None:
        try:
            vertexai.init(project=PROJECT_ID, location=REGION)
            # Try Gemini 3.0 models first, then fall back to 1.5 models
            model_names = [
                "gemini-3.0-pro",
                "gemini-3.0-flash",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "gemini-pro"  # Legacy fallback
            ]
            for model_name in model_names:
                try:
                    _gemini_model = GenerativeModel(model_name)
                    print(f"✓ Initialized {model_name} model")
                    break
                except Exception as e:
                    print(f"Warning: {model_name} failed: {e}")
                    continue
            if _gemini_model is None:
                raise Exception("All Gemini models failed to initialize")
        except Exception as e:
            print(f"Warning: Vertex AI init failed: {e}")
            _gemini_model = False  # Mark as failed to avoid retrying
    return _gemini_model if _gemini_model else None


def analyze_feedback_with_llm(feedback_data: Dict, process_data: Optional[Dict] = None) -> Dict:
    """
    Analyze feedback using Gemini to determine:
    1. Risk level (low, medium, high)
    2. Whether to auto-apply
    3. Response message
    4. Suggested changes
    
    Returns:
        {
            "risk_level": "low" | "medium" | "high",
            "auto_apply": bool,
            "response_message": str,
            "suggested_changes": dict,
            "confidence": float (0-1),
            "reasoning": str
        }
    """
    gemini_model = get_gemini_model()
    if not gemini_model:
        return {
            "risk_level": "high",
            "auto_apply": False,
            "response_message": "Thank you for your feedback. It has been received and will be reviewed.",
            "suggested_changes": {},
            "confidence": 0.0,
            "reasoning": "LLM not available"
        }
    
    process_name = feedback_data.get("processName", "Unknown")
    issue_type = feedback_data.get("issueType", "")
    suggestion = feedback_data.get("suggestion", "")
    node_ref = feedback_data.get("nodeOrEdge", "")
    rationale = feedback_data.get("rationale", "")
    
    # Build context about the process
    process_context = ""
    if process_data:
        process_context = f"""
Process Name: {process_data.get('name', 'Unknown')}
Organism: {process_data.get('organism', 'Unknown')}
Category: {process_data.get('category', 'Unknown')}
Description: {process_data.get('description', '')[:500]}
"""
    
    prompt = f"""You are analyzing feedback for a biological process flowchart system (GLMP).

PROCESS CONTEXT:
{process_context}

FEEDBACK DETAILS:
- Issue Type: {issue_type}
- Node/Edge: {node_ref if node_ref else 'Not specified'}
- Suggestion: {suggestion}
- Rationale: {rationale if rationale else 'Not provided'}

TASK: Analyze this feedback and determine:
1. RISK LEVEL: "low", "medium", or "high"
   - LOW: Simple typos, minor wording improvements, clear factual corrections
   - MEDIUM: Label changes, node additions that don't change logic
   - HIGH: Logic changes, structural modifications, controversial claims

2. AUTO-APPLY: true or false
   - true: Safe to apply automatically (low risk, clear correction)
   - false: Needs human review (medium/high risk, ambiguous, or significant change)

3. RESPONSE MESSAGE: A friendly message to the user
   - If auto-apply: Thank them and confirm the change was made
   - If not: Thank them and explain it will be reviewed

4. SUGGESTED CHANGES: JSON object with specific changes to make
   - Format: {{"type": "update_label"|"add_node"|"fix_typo"|etc, "details": {{...}}}}

5. CONFIDENCE: 0.0 to 1.0 (how confident you are in the assessment)

6. REASONING: Brief explanation of your decision

Respond ONLY with valid JSON in this exact format:
{{
    "risk_level": "low|medium|high",
    "auto_apply": true|false,
    "response_message": "message text",
    "suggested_changes": {{"type": "...", "details": {{...}}}},
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}
"""

    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            # Try parsing the whole response
            result = json.loads(response_text)
        
        # Validate and set defaults
        result.setdefault("risk_level", "high")
        result.setdefault("auto_apply", False)
        result.setdefault("response_message", "Thank you for your feedback. It will be reviewed.")
        result.setdefault("suggested_changes", {})
        result.setdefault("confidence", 0.5)
        result.setdefault("reasoning", "LLM analysis completed")
        
        return result
        
    except Exception as e:
        print(f"Error in LLM analysis: {e}")
        return {
            "risk_level": "high",
            "auto_apply": False,
            "response_message": "Thank you for your feedback. It has been received and will be reviewed.",
            "suggested_changes": {},
            "confidence": 0.0,
            "reasoning": f"LLM analysis failed: {str(e)}"
        }


def assess_risk_simple(feedback_data: Dict) -> str:
    """
    Simple rule-based risk assessment as fallback
    """
    suggestion = feedback_data.get("suggestion", "").lower()
    issue_type = feedback_data.get("issueType", "").lower()
    
    # Low risk indicators
    low_risk_keywords = ["typo", "spelling", "grammar", "capitalization", "punctuation", "wording", "phrase"]
    if any(keyword in suggestion for keyword in low_risk_keywords):
        return "low"
    
    # High risk indicators
    high_risk_keywords = ["logic", "structure", "add process", "remove", "delete", "change flow", "contradict"]
    if any(keyword in suggestion for keyword in high_risk_keywords):
        return "high"
    
    # Medium risk by default
    return "medium"


def apply_low_risk_change(process_data: Dict, change_details: Dict, feedback_data: Dict) -> Tuple[bool, str]:
    """
    Apply a low-risk change to the process JSON
    
    Returns:
        (success: bool, message: str)
    """
    change_type = change_details.get("type", "")
    
    try:
        if change_type == "update_label" or change_type == "fix_typo":
            # Update a node label
            node_id = change_details.get("details", {}).get("node_id", "")
            new_label = change_details.get("details", {}).get("new_label", "")
            
            if node_id and new_label:
                mermaid = process_data.get("mermaid", "")
                # Find and replace the node label
                # Pattern: node_id["old label"] or node_id[old label]
                pattern = rf'{re.escape(node_id)}\[([^\]]+)\]'
                replacement = f'{node_id}["{new_label}"]'
                updated_mermaid = re.sub(pattern, replacement, mermaid, count=1)
                
                if updated_mermaid != mermaid:
                    process_data["mermaid"] = updated_mermaid
                    return True, f"Updated label for node {node_id}"
        
        elif change_type == "update_description":
            # Update process description
            new_desc = change_details.get("details", {}).get("new_description", "")
            if new_desc:
                process_data["description"] = new_desc
                return True, "Updated process description"
        
        return False, "Change type not implemented or invalid"
        
    except Exception as e:
        print(f"Error applying change: {e}")
        return False, f"Error applying change: {str(e)}"


def save_process_update(process_id: str, process_data: Dict, bucket_name: str) -> bool:
    """
    Save updated process JSON to GCS
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Determine file path
        organism = process_id.split('_')[0]  # e.g., 'ecoli' from 'ecoli_lac_operon'
        file_path = f"glmp-v2/processes/{organism}/{process_id}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(process_data, indent=2),
            content_type="application/json"
        )
        
        print(f"✓ Updated process {process_id} in GCS")
        return True
        
    except Exception as e:
        print(f"Error saving process update: {e}")
        return False


def add_to_review_queue(feedback_data: Dict, analysis: Dict, bucket_name: str) -> bool:
    """
    Add feedback to review queue (stored as JSONL in GCS)
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob("glmp-feedback/review-queue.jsonl")
        
        queue_item = {
            "feedback": feedback_data,
            "analysis": analysis,
            "queued_at": feedback_data.get("receivedAt"),
            "status": "pending"
        }
        
        try:
            existing = blob.download_as_text()
        except Exception:
            existing = ""
        
        line = json.dumps(queue_item, separators=(",", ":")) + "\n"
        new_content = existing + line
        blob.upload_from_string(new_content, content_type="application/json")
        
        print(f"✓ Added feedback to review queue")
        return True
        
    except Exception as e:
        print(f"Error adding to review queue: {e}")
        return False

