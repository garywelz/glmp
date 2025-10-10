# Quick Start - Deploy GLMP Cloud Service

## 🚀 Single Command Deploy

From your desktop (with gcloud authenticated):

```bash
# 1. Get the code
cd ~/glmp-clean
git pull origin main
cd glmp-cloud-service

# 2. Deploy to Cloud Run (takes ~3-5 minutes)
gcloud run deploy glmp-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage \
  --project regal-scholar-453620-r7

# 3. Get your service URL
gcloud run services describe glmp-service \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## 🧪 Test It

```bash
# Save the URL
SERVICE_URL=$(gcloud run services describe glmp-service \
  --region us-central1 \
  --format 'value(status.url)')

# Test health
curl $SERVICE_URL/health

# List all 14 processes
curl $SERVICE_URL/api/processes

# Get Lac Operon
curl $SERVICE_URL/api/process/ecoli_lac_operon

# Validate Lac Operon
curl -X POST $SERVICE_URL/api/validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

---

## ✅ What You Get

**Working Endpoints:**
- Health check
- List all processes from GCS
- Retrieve specific process
- Validate process structure

**Foundation for:**
- Vertex AI integration (Phase 2)
- ArXiv/PubMed enrichment (Phase 2)
- Automated generation (Phase 2)

---

## 🎯 Next Steps (Tomorrow)

**Phase 2 - Add Intelligence:**

1. **Vertex AI Integration:**
   - Generate processes from paper descriptions
   - Validate biological accuracy
   - Suggest logic gates automatically

2. **Literature Enrichment:**
   - ArXiv paper search
   - PubMed citation validation
   - Automated updates

3. **Automation:**
   - Scheduled validation (Cloud Scheduler)
   - Auto-deploy on git push (Cloud Build)
   - Twitter updates (using your API key)

---

**Estimated deploy time:** 3-5 minutes  
**Cost:** ~$0 (within free tier for low traffic)  
**Status:** ✅ Ready to deploy
