# CORS Issue Summary for Cursor.com Agent

## Problem Statement

The GLMP feedback form is failing to submit due to CORS (Cross-Origin Resource Sharing) errors. The form is hosted on `https://storage.googleapis.com` and needs to POST to a Google Cloud Function at `https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback`.

## Error Messages

### Browser Console Error:
```
Access to fetch at 'https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback' 
from origin 'https://storage.googleapis.com' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### User-Facing Error:
```
❌ Error: Failed to fetch. Please check the console for details or try again later.
```

## Technical Details

### Cloud Function Configuration
- **Type**: Google Cloud Functions Gen2
- **Runtime**: Python 3.11
- **Region**: us-central1
- **Trigger**: HTTP
- **Entry Point**: `glmp_feedback`
- **Project**: regal-scholar-453620-r7
- **URL**: `https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback`

### Current Function Code
Location: `cloud-functions/glmp_feedback/main.py`

```python
import json
from datetime import datetime, timezone
from flask import make_response, Request

from google.cloud import storage

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

    # Success response with CORS headers - use tuple format
    return (json.dumps({"status": "ok"}), 200, cors_headers)
```

### Requirements File
Location: `cloud-functions/glmp_feedback/requirements.txt`
```
google-cloud-storage>=2.10.0
flask>=2.0.0
functions-framework>=3.0.0
```

### Deployment Command Used
```bash
gcloud functions deploy glmp_feedback \
  --gen2 \
  --runtime python311 \
  --region us-central1 \
  --source . \
  --entry-point glmp_feedback \
  --trigger-http \
  --allow-unauthenticated \
  --project regal-scholar-453620-r7
```

### IAM Permissions
We've also tried adding public access:
```bash
gcloud functions add-iam-policy-binding glmp_feedback \
  --gen2 \
  --region us-central1 \
  --member="allUsers" \
  --role="roles/cloudfunctions.invoker" \
  --project regal-scholar-453620-r7
```

## Testing Results

### OPTIONS Request Test:
```bash
curl -X OPTIONS "https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback" \
  -H "Origin: https://storage.googleapis.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -i
```

**Result**: 
```
HTTP/2 403 
date: Wed, 19 Nov 2025 21:10:04 GMT
content-type: text/html; charset=UTF-8
server: Google Frontend
content-length: 308

<html><head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>403 Forbidden</title>
```

**Critical Finding**: The 403 error is coming from "Google Frontend" (infrastructure layer), NOT from our function code. This means the request is being blocked at the IAM/authentication level before it even reaches the function. This is NOT a CORS issue in the code - it's an access control issue.

## What We've Tried

1. ✅ Added CORS headers to all responses (OPTIONS, POST, errors)
2. ✅ Used tuple return format `(body, status_code, headers)` for Gen2 functions
3. ✅ Used Flask's `make_response()` with explicit header setting
4. ✅ Added `Access-Control-Max-Age` header
5. ✅ Added IAM policy binding for public access (`allUsers` with `roles/cloudfunctions.invoker`)
6. ✅ Verified `--allow-unauthenticated` flag is set
7. ✅ Added Flask and functions-framework to requirements.txt

## Key Questions

1. **Why is OPTIONS request returning 403 from Google Frontend?**
   - The function is deployed with `--allow-unauthenticated`
   - IAM policy binding added: `allUsers` with `roles/cloudfunctions.invoker`
   - But OPTIONS requests are still being blocked at the infrastructure level
   - **Is there a delay in IAM policy propagation?**
   - **Do Gen2 functions require different IAM configuration?**
   - **Do OPTIONS requests need special handling in Gen2?**

2. **Is the tuple return format `(body, status_code, headers)` correct for Gen2 functions?**
   - We're using this format based on Gen2 documentation
   - But we can't test if it works because requests are blocked at 403

3. **Do Gen2 functions require different CORS configuration?**
   - Perhaps CORS needs to be configured at the Cloud Run service level (Gen2 functions run on Cloud Run) rather than in the function code?
   - Maybe we need to configure CORS in the Cloud Run service settings?

4. **Should we use a different approach?**
   - Maybe we need to use Cloud Run directly instead of Cloud Functions?
   - Or use a CORS proxy?
   - Or configure CORS in the frontend differently?
   - Or use a different authentication method?

## Frontend Code (for reference)

The frontend is making the request like this:
```javascript
const res = await fetch(FEEDBACK_ENDPOINT, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
});
```

Where `FEEDBACK_ENDPOINT = 'https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback'`

## Expected Behavior

1. Browser sends OPTIONS preflight request
2. Function returns 204 with CORS headers
3. Browser sends POST request
4. Function processes feedback and returns 200 with CORS headers
5. Form shows success message

## Current Behavior

1. Browser sends OPTIONS preflight request
2. ❌ Function returns 403 Forbidden (blocked before reaching code)
3. Browser blocks the request due to CORS policy violation
4. Form shows "Failed to fetch" error

## Files to Review

- `cloud-functions/glmp_feedback/main.py` - Function code
- `cloud-functions/glmp_feedback/requirements.txt` - Dependencies
- `glmp-v2/viewer/viewer.js` - Frontend code (lines ~911-912 for fetch call)

## Additional Context

- The viewer is successfully deployed and working
- Process ID display is working
- Node click-to-fill is working
- Only the form submission is failing due to CORS

## Update: IAM Binding Attempts

We've tried multiple approaches to add the `roles/run.invoker` permission:

1. ✅ `gcloud run services add-iam-policy-binding glmp-feedback` (with hyphen)
2. ✅ `gcloud run services add-iam-policy-binding glmp_feedback` (with underscore)  
3. ✅ `gcloud functions add-invoker-policy-binding glmp_feedback` (without --gen2)
4. ✅ `gcloud functions add-invoker-policy-binding glmp_feedback --gen2` (with --gen2 flag)

**Still getting 403 Forbidden** - The OPTIONS request is still being blocked at the Google Frontend level.

**Question**: How do we find the actual Cloud Run service name for a Gen2 function? The service name might be auto-generated and different from the function name.

## Request for Cursor.com Agent

Please help diagnose why:
1. **OPTIONS requests are returning 403 from Google Frontend** - The request is being blocked at the infrastructure/IAM level before reaching our function code. Even though we've:
   - Set `--allow-unauthenticated` in deployment
   - Added IAM policy binding for `allUsers` with `roles/cloudfunctions.invoker`
   - The 403 is coming from "Google Frontend", not our function
   
2. **How to properly configure public access for Gen2 Cloud Functions** - Is there a different way to make Gen2 functions publicly accessible?

3. **Whether Gen2 functions require different CORS configuration** - Should CORS be configured at the Cloud Run service level instead of in the function code?

4. **Alternative approaches** - Should we:
   - Use Cloud Run directly instead of Cloud Functions?
   - Use a different authentication/authorization method?
   - Configure CORS differently?

Any insights, alternative approaches, or specific Gen2 configuration requirements would be greatly appreciated!
