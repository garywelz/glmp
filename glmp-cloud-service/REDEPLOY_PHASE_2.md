# Redeploy with Phase 2 Features

## 🚀 Deploy Updated Service

The service now includes **Vertex AI, ArXiv, and PubMed integration!**

### **Deploy Command:**

```bash
cd ~/glmp-clean/glmp-cloud-service
git pull origin main

gcloud run deploy glmp-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage \
  --project regal-scholar-453620-r7 \
  --memory 1Gi \
  --timeout 600 \
  --cpu 2
```

**Changes from Phase 1:**
- `--memory 1Gi` (was 512Mi) - For Vertex AI models
- `--timeout 600` (was 300) - 10 minutes for AI operations
- `--cpu 2` (was 1) - Faster AI inference

**Deploy time:** ~4-6 minutes

---

## 🧪 Test Phase 2 Features

After deployment completes, test the new capabilities:

```bash
# Run comprehensive test suite
./test_service.sh
```

Or test individual features:

### **1. Generate New Process (Vertex AI):**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yeast GAL Gene Regulation",
    "organism": "S. cerevisiae",
    "category": "Gene Regulation",
    "description": "GAL genes encode galactose metabolism enzymes. Regulated by Gal4 activator and Gal80 repressor.",
    "save_to_gcs": false
  }'
```

### **2. Validate Citations (PubMed):**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/validate-citations \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

### **3. Search ArXiv:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-arxiv \
  -H "Content-Type: application/json" \
  -d '{"query": "bacterial gene regulation", "max_results": 5, "category": "q-bio"}'
```

### **4. AI Validation:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/ai-validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

---

## ✅ Expected Results

### **After Deployment:**

**New Endpoints Available:**
- ✅ `/api/generate` - Generate processes with AI
- ✅ `/api/ai-validate` - AI-powered validation
- ✅ `/api/search-arxiv` - Search ArXiv
- ✅ `/api/search-pubmed` - Search PubMed
- ✅ `/api/validate-citations` - Citation validation
- ✅ `/api/enrich` - Full literature enrichment

**Service Info Response:**
```json
{
  "service": "GLMP Cloud Service",
  "version": "2.0.0",
  "status": "healthy",
  "features": {
    "vertex_ai": true,
    "arxiv": true,
    "pubmed": true,
    "secret_manager": true
  }
}
```

---

## 🎯 What You Can Do Now

### **Immediate:**
1. **Generate new processes** - Just provide description, AI does the rest
2. **Validate existing processes** - Check biological accuracy
3. **Find recent papers** - ArXiv and PubMed search
4. **Validate citations** - Ensure all PMIDs are correct

### **Automation:**
1. **Nightly jobs** - Validate all processes
2. **Literature watch** - Monitor for new papers
3. **Auto-generation** - Create processes from literature
4. **Quality control** - AI-powered consistency checks

---

## 🔧 Troubleshooting

### If deployment fails:
```bash
# Check build logs
gcloud builds list --limit 5

# View specific build
gcloud builds log <BUILD_ID>
```

### If Vertex AI fails:
```bash
# Check service logs
gcloud run services logs read glmp-service --region us-central1 --limit 100

# Verify Vertex AI permissions
gcloud projects get-iam-policy regal-scholar-453620-r7 \
  --flatten="bindings[].members" \
  --filter="bindings.role:roles/aiplatform.user"
```

---

## 📊 Cost Estimate

**Cloud Run:** ~$0.01/hour (low traffic)  
**Vertex AI:** ~$0.0025 per 1K characters (Gemini Pro)  
**Storage:** ~$0.02/GB/month  
**Total:** Likely under **$5/month** for moderate use

---

**Ready to unlock AI-powered process generation!** 🤖✨
