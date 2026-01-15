# GLMP Feedback Hybrid System - Implementation Guide

## Overview

This implements **Option 3: Hybrid Approach** for processing feedback:
- ✅ **Auto-respond** to all feedback with LLM-generated messages
- ✅ **Auto-apply** low-risk changes (typos, minor wording)
- ✅ **Flag** significant changes for manual review

## Architecture

### Components

1. **`main.py`** - Main Cloud Function endpoint
   - Receives feedback from viewer
   - Logs to GCS
   - Triggers LLM processing (non-blocking)

2. **`feedback_processor.py`** - LLM Analysis Engine
   - Uses Vertex AI Gemini to analyze feedback
   - Determines risk level (low/medium/high)
   - Suggests changes
   - Applies low-risk changes automatically

3. **`email_sender.py`** - Email Notification System
   - Queues emails for sending
   - Processes email queue (via Cloud Scheduler)
   - Uses Gmail API

## How It Works

### 1. Feedback Submission Flow

```
User submits feedback
    ↓
Cloud Function receives POST
    ↓
Logs to feedback.jsonl
    ↓
Triggers LLM analysis (async)
    ↓
Returns success to user immediately
```

### 2. LLM Analysis Flow

```
Load process data from GCS
    ↓
Analyze with Gemini:
  - Risk assessment
  - Auto-apply decision
  - Response message generation
    ↓
If LOW RISK + HIGH CONFIDENCE:
  → Auto-apply change
  → Save updated process
  → Queue thank-you email
    ↓
If MEDIUM/HIGH RISK:
  → Add to review queue
  → Queue acknowledgment email
```

### 3. Risk Assessment Criteria

**LOW RISK** (auto-apply):
- Simple typos and spelling errors
- Minor wording improvements
- Clear factual corrections
- Capitalization fixes
- Punctuation corrections

**MEDIUM RISK** (review queue):
- Label changes
- Node additions that don't change logic
- Description updates
- Citation additions

**HIGH RISK** (review queue):
- Logic changes
- Structural modifications
- Controversial claims
- Process flow changes
- Node deletions

## Configuration

### Environment Variables

```bash
# Required
PROJECT_ID=regal-scholar-453620-r7
BUCKET_NAME=regal-scholar-453620-r7-podcast-storage

# Optional (for email)
GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
GMAIL_TOKEN_PATH=/path/to/token.json
```

### GCS Structure

```
gs://bucket/
  glmp-feedback/
    feedback.jsonl          # All feedback (with LLM analysis)
    review-queue.jsonl      # Items needing manual review
    email-queue.jsonl       # Emails to send
```

## Deployment

### 1. Deploy Cloud Function

```bash
cd cloud-functions/glmp_feedback

gcloud functions deploy glmp_feedback \
  --gen2 \
  --runtime python311 \
  --region us-central1 \
  --source . \
  --entry-point glmp_feedback \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage \
  --timeout 540s \
  --memory 512Mi
```

### 2. Set Up Cloud Scheduler (for email processing)

```bash
# Create a Cloud Scheduler job to process email queue every 5 minutes
gcloud scheduler jobs create http process-email-queue \
  --location=us-central1 \
  --schedule="*/5 * * * *" \
  --uri="https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_email_processor" \
  --http-method=POST \
  --oidc-service-account-email=YOUR_SERVICE_ACCOUNT@regal-scholar-453620-r7.iam.gserviceaccount.com
```

### 3. Set Up Gmail API (Optional)

1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Download credentials JSON
4. Store in Secret Manager or upload to Cloud Function

## Testing

### Test Feedback Submission

```bash
curl -X POST https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback \
  -H "Content-Type: application/json" \
  -d '{
    "processId": "ecoli_lac_operon",
    "processName": "Lac Operon",
    "issueType": "typo",
    "suggestion": "Fix spelling: 'operon' should be 'operon'",
    "nodeOrEdge": "A1",
    "email": "test@example.com",
    "okToContact": true
  }'
```

### Check Feedback Log

```bash
gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-feedback/feedback.jsonl | tail -1 | jq .
```

### Check Review Queue

```bash
gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-feedback/review-queue.jsonl | jq .
```

## Monitoring

### Cloud Logging Queries

**View all feedback processing:**
```
resource.type="cloud_function"
resource.labels.function_name="glmp_feedback"
textPayload=~"LLM Analysis"
```

**View auto-applied changes:**
```
resource.type="cloud_function"
resource.labels.function_name="glmp_feedback"
textPayload=~"Auto-applying"
```

**View review queue additions:**
```
resource.type="cloud_function"
resource.labels.function_name="glmp_feedback"
textPayload=~"Adding to review queue"
```

## Manual Review Process

1. **Check Review Queue:**
   ```bash
   gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-feedback/review-queue.jsonl | jq .
   ```

2. **Review Each Item:**
   - Read feedback and LLM analysis
   - Check suggested changes
   - Verify against scientific sources

3. **Apply Changes:**
   - Manually update process JSON
   - Deploy to GCS
   - Remove from review queue

4. **Send Response:**
   - Email user with decision
   - Thank them for contribution

## Safety Features

1. **Confidence Threshold:** Only auto-apply if confidence > 0.7
2. **Risk Level Check:** Only auto-apply low-risk changes
3. **Process Validation:** Verify process JSON is valid before saving
4. **Backup:** Original process is preserved (can be restored)
5. **Audit Trail:** All changes logged with timestamps

## Future Enhancements

- [ ] Web UI for review queue
- [ ] Automated testing before auto-apply
- [ ] Multi-language support
- [ ] Expert reviewer assignment
- [ ] Change history tracking
- [ ] Rollback capability



