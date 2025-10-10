# Deploy GLMP Service to Cloud Run

## ✅ Prerequisites

1. **Google Cloud SDK** installed (you already have this)
2. **Service account** with permissions:
   - Cloud Run Admin
   - Storage Object Admin
   - Secret Manager Secret Accessor
3. **Authenticated** with gcloud

---

## 🚀 Quick Deploy (Option 1 - Easiest)

```bash
cd ~/glmp-clean/glmp-cloud-service

# Deploy directly from source
gcloud run deploy glmp-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage \
  --memory 512Mi \
  --timeout 300 \
  --service-account garywelz@regal-scholar-453620-r7.iam.gserviceaccount.com
```

This will:
- Build the container automatically
- Push to Container Registry
- Deploy to Cloud Run
- Give you a URL like: `https://glmp-service-XXXXX-uc.a.run.app`

---

## 🔧 Manual Build & Deploy (Option 2)

```bash
cd ~/glmp-clean/glmp-cloud-service

# Build container
gcloud builds submit --tag gcr.io/regal-scholar-453620-r7/glmp-service

# Deploy to Cloud Run
gcloud run deploy glmp-service \
  --image gcr.io/regal-scholar-453620-r7/glmp-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage
```

---

## 🧪 Test After Deployment

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe glmp-service \
  --region us-central1 \
  --format 'value(status.url)')

echo "Service URL: $SERVICE_URL"

# Test health check
curl $SERVICE_URL/health

# List processes
curl $SERVICE_URL/api/processes

# Get specific process
curl $SERVICE_URL/api/process/ecoli_lac_operon

# Validate a process
curl -X POST $SERVICE_URL/api/validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

---

## 📋 Expected Responses

### Health Check:
```json
{
  "status": "healthy",
  "checks": {
    "storage": true,
    "secrets": true
  },
  "timestamp": "2025-10-10T13:52:00.000Z"
}
```

### List Processes:
```json
{
  "success": true,
  "count": 14,
  "processes": [
    "glmp-v2/processes/ecoli/ecoli_lac_operon.json",
    "glmp-v2/processes/ecoli/ecoli_dna_replication_initiation.json",
    ...
  ]
}
```

### Validate Process:
```json
{
  "success": true,
  "process_id": "ecoli_lac_operon",
  "valid": true,
  "checks": {
    "has_id": true,
    "has_name": true,
    "has_mermaid": true,
    "has_sources": true,
    "node_count": 63,
    "logic_gate_count": 7
  }
}
```

---

## 🔐 Service Account Setup

If you don't have the service account configured:

```bash
# Create service account (if needed)
gcloud iam service-accounts create glmp-service \
  --display-name "GLMP Cloud Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding regal-scholar-453620-r7 \
  --member serviceAccount:glmp-service@regal-scholar-453620-r7.iam.gserviceaccount.com \
  --role roles/storage.objectAdmin

gcloud projects add-iam-policy-binding regal-scholar-453620-r7 \
  --member serviceAccount:glmp-service@regal-scholar-453620-r7.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding regal-scholar-453620-r7 \
  --member serviceAccount:glmp-service@regal-scholar-453620-r7.iam.gserviceaccount.com \
  --role roles/aiplatform.user
```

---

## ⚙️ Configuration

### Environment Variables:
- `PROJECT_ID`: `regal-scholar-453620-r7`
- `BUCKET_NAME`: `regal-scholar-453620-r7-podcast-storage`
- `PORT`: `8080` (Cloud Run default)

### Resources:
- Memory: 512Mi (can increase for Vertex AI workloads)
- Timeout: 300s (5 min for complex operations)
- Concurrency: 80 (Cloud Run default)

---

## 🐛 Troubleshooting

### If deployment fails:
```bash
# Check Cloud Build logs
gcloud builds list --limit 5

# View specific build
gcloud builds log <BUILD_ID>
```

### If service is unhealthy:
```bash
# Check logs
gcloud run services logs read glmp-service --region us-central1 --limit 50

# Check service details
gcloud run services describe glmp-service --region us-central1
```

### If can't access GCS:
```bash
# Verify service account has permissions
gcloud projects get-iam-policy regal-scholar-453620-r7 \
  --flatten="bindings[].members" \
  --filter="bindings.members:glmp-service@*"
```

---

## 📊 Next Steps After Deployment

1. **Verify all endpoints work**
2. **Test validation on all 14 processes**
3. **Add Vertex AI integration** (Phase 2)
4. **Add ArXiv/PubMed enrichment** (Phase 2)
5. **Set up GitHub CI/CD** (auto-deploy on push)

---

## 🔗 Integration with GLMP Viewer

Once deployed, you could add features like:

```javascript
// In viewer.js - validate process before rendering
async function validateProcess(processId) {
  const response = await fetch(
    `https://glmp-service-XXXXX-uc.a.run.app/api/validate`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ process_id: processId })
    }
  );
  
  const result = await response.json();
  return result.valid;
}
```

---

**Ready to deploy?** Run the Quick Deploy command and let me know what URL you get! 🚀
