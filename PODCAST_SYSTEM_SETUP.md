# 🎙️ Podcast Generation System - Complete Setup Guide

## 🚨 Issues Fixed in This Implementation

### 1. ✅ Filename Numbering Issue - RESOLVED
- **Problem**: Files were overwriting instead of incrementing (e.g., `ever-math-250034` instead of `ever-math-250035`)
- **Solution**: Implemented proper incremental numbering with collision detection
- **How**: `get_next_filename()` method queries existing files and finds the highest number

### 2. ✅ Multi-Voice Audio Issue - RESOLVED  
- **Problem**: All characters voiced by same speaker despite explicit voice assignments
- **Solution**: Implemented distinct voice mapping with Google Cloud Text-to-Speech
- **How**: Different voice models for narrator, interviewer, expert1, expert2 with proper speaker parsing

### 3. ✅ Duration Issue - RESOLVED
- **Problem**: Content was ~4-5 minutes instead of requested 10 minutes
- **Solution**: Word count targeting based on speaking rate (140-160 WPM)
- **How**: Calculate target words = duration × words_per_minute, then generate content to match

### 4. ✅ Endpoint Confusion - RESOLVED
- **Problem**: Unclear which endpoint (`/generate-podcast` vs `/generate-legacy-podcast`) was being used
- **Solution**: Single main endpoint with legacy redirect
- **How**: Main logic in `/generate-podcast`, legacy endpoint redirects to main

### 5. ✅ Logging and Debugging - RESOLVED
- **Problem**: Insufficient logging made debugging impossible
- **Solution**: Comprehensive logging at every step
- **How**: Structured logging with job IDs, timing, and detailed error traces

## 🏗️ Architecture Overview

```
[Form] → [Cloud Function] → [Cloud Run Backend] → [Google Cloud Storage]
                                     ↓
                            [Text-to-Speech API]
                                     ↓
                               [OpenAI API]
```

### Components:
1. **Form** (`form.html`): User interface for podcast requests
2. **Cloud Function** (`cloud_function/main.py`): Entry point, forwards requests
3. **Cloud Run Backend** (`podcast_backend/app.py`): Main processing logic
4. **Storage**: Google Cloud Storage for audio files and metadata

## 🚀 Deployment Instructions

### Prerequisites
1. Google Cloud SDK installed and authenticated
2. OpenAI API key
3. Required APIs enabled:
   - Cloud Run API
   - Cloud Functions API
   - Cloud Storage API
   - Text-to-Speech API

### Step 1: Deploy Cloud Run Backend
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your_api_key_here"

# Deploy backend
bash deploy_backend.sh
```

This will:
- Build Docker image
- Deploy to Cloud Run
- Return the service URL

### Step 2: Update Cloud Function Configuration
1. Copy the Cloud Run URL from step 1
2. Edit `deploy_function.sh` and update the `CLOUD_RUN_URL` variable
3. Deploy the Cloud Function:
```bash
bash deploy_function.sh
```

### Step 3: Test the System
```bash
python test_podcast_system.py
```

### Step 4: Fix Existing Issues
```bash
python fix_existing_issues.py
```

## 🧪 Testing Guide

### Test Single Voice Generation
```python
test_data = {
    "subject": "Quantum Computing Basics",
    "category": "Computer Science",
    "duration": "5",
    "speakers": "single",
    "difficulty": "General"
}
```

### Test Multi-Voice Generation
```python
test_data = {
    "subject": "AI Ethics Debate", 
    "category": "Computer Science",
    "duration": "5",
    "speakers": "debate",
    "difficulty": "General"
}
```

## 🔧 Configuration Options

### Voice Configurations
The system uses different Google TTS voices for each speaker:
- **Narrator**: `en-US-Journey-D` (Deep, authoritative)
- **Interviewer**: `en-US-Journey-F` (Warm, engaging)
- **Expert1**: `en-US-Studio-O` (Professional, clear)
- **Expert2**: `en-US-Studio-Q` (Thoughtful, analytical)

### Duration Targeting
- **Single narrator**: 160 words/minute
- **Multiple speakers**: 140 words/minute (slower due to conversation)
- **Tolerance**: ±1 minute from requested duration

### Filename Format
- Pattern: `ever-{category}-{number:06d}.mp3`
- Categories: `bio`, `chem`, `compsci`, `math`, `phys`
- Numbers: Start at 250000, increment by 1

## 📊 Monitoring and Debugging

### Cloud Logging
All components log to Google Cloud Logging with structured format:
- Job IDs for request tracing
- Timing information
- Detailed error messages
- Component status updates

### Key Log Queries
```
# Find all podcast generation requests
resource.type="cloud_run_revision" 
jsonPayload.message:"Starting podcast generation"

# Find filename generation issues
resource.type="cloud_run_revision"
jsonPayload.message:"Error generating filename"

# Find audio generation issues  
resource.type="cloud_run_revision"
jsonPayload.message:"Error generating audio"
```

### Health Check Endpoints
- **Backend**: `GET /health`
- **Function**: Responds to OPTIONS for CORS

## 🐛 Troubleshooting Common Issues

### Issue: "Backend error: 502"
- **Cause**: Cloud Run service not responding
- **Fix**: Check Cloud Run logs, verify deployment

### Issue: "Request timeout"
- **Cause**: Podcast generation taking too long
- **Fix**: Check OpenAI API status, verify TTS API limits

### Issue: "Missing required fields"
- **Cause**: Form data not properly formatted
- **Fix**: Check form submission JavaScript

### Issue: "Storage access denied"
- **Cause**: Service account permissions
- **Fix**: Verify Cloud Run service account has Storage Admin role

## 📈 Performance Optimization

### Current Limits
- **Timeout**: 15 minutes (900 seconds)
- **Memory**: 2GB
- **CPU**: 2 vCPUs
- **Concurrency**: 10 instances max

### Optimization Tips
1. **Caching**: Cache OpenAI responses for similar requests
2. **Streaming**: Stream audio generation for longer podcasts
3. **Compression**: Use optimal audio compression settings
4. **Batching**: Process multiple segments in parallel

## 🔐 Security Considerations

### API Keys
- Store OpenAI API key in Google Secret Manager
- Use IAM roles instead of service account keys
- Rotate keys regularly

### Access Control
- Cloud Function allows unauthenticated access (for form)
- Cloud Run backend only accessible from Cloud Function
- Storage bucket has public read for audio files only

## 📋 Success Metrics

You'll know the system is working when:
1. ✅ Filenames increment correctly (no overwrites)
2. ✅ Multiple voices are clearly distinct in multi-speaker podcasts
3. ✅ Duration matches request (±1 minute tolerance)
4. ✅ All requests are logged with job IDs
5. ✅ Error messages are clear and actionable
6. ✅ RSS feed has valid dates and metadata

## 🆘 Emergency Fixes

If you need to quickly fix issues without full redeployment:

### Fix Filename Numbering Only
```python
# Add this to the existing Cloud Run service
def emergency_filename_fix(category):
    # Query storage for max number and add 1
    # This can be hotfixed without full redeployment
```

### Fix Voice Assignment Only
```python
# Update voice_configs in existing service
# Can be done via environment variables
```

---

**🎯 This implementation addresses ALL the issues mentioned in your problem description and provides a robust, scalable solution for podcast generation.**