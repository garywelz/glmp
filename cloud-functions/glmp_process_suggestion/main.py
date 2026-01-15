"""
Cloud Function for Process Suggestion Chat
Handles interactive chat to clarify process suggestions and generate processes
"""

import json
from datetime import datetime, timezone
from flask import Request
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = "regal-scholar-453620-r7"
REGION = "us-central1"
BUCKET_NAME = "regal-scholar-453620-r7-podcast-storage"

def get_gemini_model():
    """Get or initialize Gemini model (lazy initialization with error handling)"""
    global gemini_model
    if gemini_model is None:
        try:
            vertexai.init(project=PROJECT_ID, location=REGION)
            # Try Gemini 3.0 models first, then fall back to 1.5 models
            model_names = [
                "gemini-3.0-pro",
                "gemini-3.0-flash", 
                "gemini-1.5-pro",
                "gemini-1.5-flash"
            ]
            for model_name in model_names:
                try:
                    gemini_model = GenerativeModel(model_name)
                    print(f"✓ Initialized {model_name} model")
                    break
                except Exception as e:
                    print(f"Warning: {model_name} failed: {e}")
                    continue
            if gemini_model is None:
                raise Exception("All Gemini models failed to initialize")
        except Exception as e:
            print(f"Warning: Vertex AI init failed: {e}")
            gemini_model = False  # Mark as failed
    return gemini_model if gemini_model else None

# Initialize model variable
gemini_model = None

storage_client = storage.Client()


def glmp_process_suggestion(request: Request):
    """HTTP Cloud Function to handle process suggestion chat"""
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

    session_id = data.get("sessionId")
    action = data.get("action")
    
    if action == "approve":
        # Generate the process
        return handle_approval(data, cors_headers)
    else:
        # Handle chat message
        return handle_chat_message(data, cors_headers)


def handle_chat_message(data: dict, cors_headers: dict):
    """Handle a chat message and respond with clarification or process description"""
    session_id = data.get("sessionId")
    message = data.get("message", "").strip()
    current_suggestion = data.get("currentSuggestion")
    
    if not message:
        return (json.dumps({"error": "Message required"}), 400, cors_headers)
    
    gemini_model = get_gemini_model()
    if not gemini_model:
        return (json.dumps({
            "type": "error",
            "message": "AI service temporarily unavailable. Please try again later."
        }), 500, cors_headers)
    
    # Load conversation history from session
    conversation = load_conversation(session_id)
    conversation.append({"role": "user", "content": message})
    
    # Build prompt for LLM
    if current_suggestion:
        # We have a process description, just need to confirm
        prompt = f"""You are helping a user suggest a biological process for the GLMP collection.

Current process suggestion:
- Name: {current_suggestion.get('name', 'Unknown')}
- Organism: {current_suggestion.get('organism', 'Unknown')}
- Category: {current_suggestion.get('category', 'Unknown')}
- Description: {current_suggestion.get('description', '')}

User just said: "{message}"

If the user is confirming/approving, respond with "APPROVE" and the process is ready.
If the user wants changes, ask what they'd like to modify.
If unclear, ask for clarification.

Respond in a friendly, conversational way."""
    else:
        # Build conversation context
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation[-5:]])
        
        prompt = f"""You are helping a user suggest a biological process for the GLMP collection.

Conversation so far:
{context}

Your task:
1. Ask clarifying questions to understand:
   - What specific biological process?
   - Which organism? (E. coli, S. cerevisiae, human, etc.)
   - What category? (Gene Regulation, Metabolism, Stress Response, etc.)
   - Any specific aspects to focus on?

2. Once you have enough information, propose a complete process description in this format:
   PROCESS_READY:
   Name: [Process Name]
   Organism: [Organism]
   Category: [Category]
   Description: [2-3 sentence detailed description]

3. Keep questions concise and friendly. Ask one question at a time if possible.

User's latest message: "{message}"

Respond naturally, as if having a conversation."""
    
    try:
        model = get_gemini_model()
        if not model:
            raise Exception("No Gemini model available")
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Check if process is ready
        if "PROCESS_READY:" in response_text or current_suggestion:
            # Extract or use current process
            if "PROCESS_READY:" in response_text:
                process = extract_process_from_response(response_text)
            else:
                process = current_suggestion
            
            if process:
                # Save conversation
                conversation.append({"role": "assistant", "content": response_text})
                save_conversation(session_id, conversation)
                
                return (json.dumps({
                    "type": "process_ready",
                    "message": "I've prepared a process description based on our conversation. Please review it below and let me know if you'd like to approve it or make changes.",
                    "process": process
                }), 200, cors_headers)
        
        # Still clarifying
        conversation.append({"role": "assistant", "content": response_text})
        save_conversation(session_id, conversation)
        
        return (json.dumps({
            "type": "clarification",
            "message": response_text
        }), 200, cors_headers)
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return (json.dumps({
            "type": "error",
            "message": f"Sorry, I encountered an error: {str(e)}"
        }), 500, cors_headers)


def extract_process_from_response(response_text: str) -> dict:
    """Extract process details from LLM response"""
    try:
        lines = response_text.split('\n')
        process = {}
        
        for line in lines:
            if line.startswith('Name:'):
                process['name'] = line.split('Name:')[1].strip()
            elif line.startswith('Organism:'):
                process['organism'] = line.split('Organism:')[1].strip()
            elif line.startswith('Category:'):
                process['category'] = line.split('Category:')[1].strip()
            elif line.startswith('Description:'):
                process['description'] = line.split('Description:')[1].strip()
        
        # If we didn't get all fields, try to infer
        if not process.get('name'):
            # Try to extract from first line after PROCESS_READY
            parts = response_text.split('PROCESS_READY:')
            if len(parts) > 1:
                first_line = parts[1].split('\n')[0].strip()
                if ':' in first_line:
                    process['name'] = first_line.split(':', 1)[1].strip()
        
        # Defaults if missing
        process.setdefault('organism', 'E. coli')
        process.setdefault('category', 'Metabolic Pathway')
        
        if process.get('name') and process.get('description'):
            return process
        return None
        
    except Exception as e:
        print(f"Error extracting process: {e}")
        return None


def handle_approval(data: dict, cors_headers: dict):
    """Handle process approval and generate the full process JSON"""
    process = data.get("process")
    session_id = data.get("sessionId")
    
    if not process:
        return (json.dumps({"error": "Process data required"}), 400, cors_headers)
    
    gemini_model = get_gemini_model()
    if not gemini_model:
        return (json.dumps({"error": "AI service unavailable"}), 500, cors_headers)
    
    try:
        # Generate full process using ProcessGenerator logic
        process_json = generate_process_json(process)
        
        if not process_json:
            return (json.dumps({"error": "Failed to generate process"}), 500, cors_headers)
        
        # Save to GCS
        process_id = process_json.get("id", f"{process['organism'].lower().replace(' ', '_')}_{process['name'].lower().replace(' ', '_')}")
        organism_dir = process['organism'].lower().replace(' ', '_').replace('.', '')
        if 'ecoli' in organism_dir or 'e. coli' in organism_dir.lower():
            organism_dir = 'ecoli'
        elif 'yeast' in organism_dir or 's. cerevisiae' in organism_dir.lower():
            organism_dir = 'yeast'
        
        file_path = f"glmp-v2/processes/{organism_dir}/{process_id}.json"
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(process_json, indent=2),
            content_type="application/json"
        )
        
        # Update metadata (async - don't block)
        try:
            update_metadata(process_json)
        except Exception as e:
            print(f"Warning: Could not update metadata: {e}")
        
        # Add notification comment
        try:
            add_notification_comment(process_id, process_json.get("name", "New Process"))
        except Exception as e:
            print(f"Warning: Could not add notification comment: {e}")
        
        return (json.dumps({
            "status": "success",
            "processId": process_id,
            "message": "Process generated and saved successfully"
        }), 200, cors_headers)
        
    except Exception as e:
        print(f"Error generating process: {e}")
        return (json.dumps({"error": str(e)}), 500, cors_headers)


def generate_process_json(process: dict) -> dict:
    """Generate full process JSON using Vertex AI"""
    name = process.get("name", "")
    organism = process.get("organism", "E. coli")
    category = process.get("category", "Metabolic Pathway")
    description = process.get("description", "")
    
    prompt = f"""You are a biological process expert. Generate a detailed biological process flowchart in JSON format.

PROCESS DETAILS:
- Name: {name}
- Organism: {organism}
- Category: {category}
- Description: {description}

REQUIREMENTS:
1. Create a Mermaid flowchart with 30-50 unique nodes (use IDs: A, B, C, ..., AA, AB, etc.)
2. Identify all logic gates:
   - OR gates: Single input, binary yes/no decision (diamond shape)
   - AND gates: Multiple inputs converging (diamond shape with multiple arrows in)
3. Apply 7-color scheme:
   - Red (#ff6b6b): Triggers & Inputs
   - Yellow (#ffd43b): Structures & Objects (proteins, enzymes)
   - Green (#51cf66): Processing & Operations
   - Blue (#74c0fc): Intermediates & States
   - Orange (#ff9f43): OR Logic Gates (diamonds)
   - Lavender (#b4b4dc): AND Logic Gates (diamonds)
   - Violet (#b197fc): Products & Outputs
4. Style EVERY node explicitly
5. Include 3-5 scientific citations with PubMed IDs
6. Add scientific accuracy statement
7. Count nodes and logic gates

Generate ONLY valid JSON matching this exact schema:
{{
  "id": "organism_process_name",
  "name": "Process Name",
  "organism": "Organism",
  "category": "Category",
  "description": "Detailed description",
  "scientificAccuracy": "Statement about validation",
  "complexity": {{
    "nodes": 0,
    "uniqueIdentifiers": true,
    "colorCoded": true,
    "detailLevel": "detailed",
    "logicGates": {{"orGates": 0, "andGates": 0, "total": 0}}
  }},
  "colorScheme": {{
    "red": {{"hex": "#ff6b6b", "category": "Triggers & Inputs", "description": "..."}},
    "yellow": {{"hex": "#ffd43b", "category": "Structures & Objects", "description": "..."}},
    "green": {{"hex": "#51cf66", "category": "Processing & Operations", "description": "..."}},
    "blue": {{"hex": "#74c0fc", "category": "Intermediates & States", "description": "..."}},
    "orange": {{"hex": "#ff9f43", "category": "OR Logic Gates", "description": "..."}},
    "lavender": {{"hex": "#b4b4dc", "category": "AND Logic Gates", "description": "..."}},
    "violet": {{"hex": "#b197fc", "category": "Products & Outputs", "description": "..."}}
  }},
  "mermaid": "graph TD\\n...",
  "sources": [{{"authors": "...", "title": "...", "journal": "...", "year": "...", "pmid": "..."}}],
  "created": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
  "verified": false
}}

Generate the complete JSON now:"""

    try:
        model = get_gemini_model()
        if not model:
            return None
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        process_data = json.loads(response_text.strip())
        
        # Ensure ID is set correctly
        if not process_data.get("id"):
            process_data["id"] = f"{organism.lower().replace(' ', '_').replace('.', '')}_{name.lower().replace(' ', '_')}"
        
        return process_data
        
    except Exception as e:
        print(f"Error generating process JSON: {e}")
        return None


def load_conversation(session_id: str) -> list:
    """Load conversation history from GCS"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"glmp-process-suggestions/sessions/{session_id}.json")
        if blob.exists():
            content = blob.download_as_text()
            data = json.loads(content)
            return data.get("conversation", [])
    except Exception:
        pass
    return []


def save_conversation(session_id: str, conversation: list):
    """Save conversation history to GCS"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"glmp-process-suggestions/sessions/{session_id}.json")
        data = {
            "sessionId": session_id,
            "conversation": conversation,
            "lastUpdated": datetime.now(timezone.utc).isoformat()
        }
        blob.upload_from_string(
            json.dumps(data, indent=2),
            content_type="application/json"
        )
    except Exception as e:
        print(f"Error saving conversation: {e}")


def update_metadata(process_json: dict):
    """Update metadata.json to include new process"""
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob("glmp-v2/metadata.json")
        
        if blob.exists():
            metadata = json.loads(blob.download_as_text())
        else:
            metadata = {"processes": []}
        
        # Add new process with all required fields for the table
        complexity = process_json.get("complexity", {})
        logic_gates = complexity.get("logicGates", {})
        
        process_entry = {
            "id": process_json.get("id"),
            "name": process_json.get("name"),
            "organism": process_json.get("organism"),
            "category": process_json.get("category"),
            "nodes": complexity.get("nodes", 0),
            "conditionals": 0,  # Will be calculated if needed
            "logicGates": {
                "or": logic_gates.get("orGates", 0),
                "and": logic_gates.get("andGates", 0)
            },
            "notGates": 0,  # Will be calculated if needed
            "complexity": "detailed"  # Default complexity level
        }
        
        if "processes" not in metadata:
            metadata["processes"] = []
        
        # Check if already exists
        existing_ids = [p.get("id") for p in metadata["processes"]]
        if process_entry["id"] not in existing_ids:
            metadata["processes"].append(process_entry)
            blob.upload_from_string(
                json.dumps(metadata, indent=2),
                content_type="application/json"
            )
    except Exception as e:
        print(f"Error updating metadata: {e}")


def add_notification_comment(process_id: str, process_name: str):
    """Add a notification comment to the process page"""
    try:
        from comments_storage import save_comment
        
        comment = {
            "author": "GLMP System",
            "role": "system",
            "issueType": "notification",
            "suggestion": f"Process '{process_name}' was generated from a user suggestion and added to the collection.",
            "status": "applied",
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
        
        save_comment(process_id, comment, BUCKET_NAME)
    except Exception as e:
        print(f"Error adding notification comment: {e}")

