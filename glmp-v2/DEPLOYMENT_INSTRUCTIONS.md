# GLMP v2 - Deployment Instructions

## Quick Deployment (Recommended)

The remote environment has **read-only** access to GCS. You need to deploy from an environment with write permissions.

---

## 🚀 Method 1: Use the Deployment Script (Easiest)

### Step 1: Get the Files

**On your local machine:**

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/garywelz/glmp.git
cd glmp

# Switch to the clean-slate branch
git checkout clean-slate-v2-viewer-system

# Navigate to the v2 directory
cd glmp-v2
```

### Step 2: Authenticate

**Option A: Service Account (Recommended for automation)**

```bash
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json
gcloud config set project regal-scholar-453620-r7
```

**Option B: User Account (Interactive)**

```bash
gcloud auth login
gcloud config set project regal-scholar-453620-r7
```

### Step 3: Run the Deployment Script

```bash
./DEPLOY_TO_GCS.sh
```

That's it! The script will:
- ✅ Verify authentication
- ✅ Upload all files
- ✅ Set public permissions
- ✅ Configure cache headers
- ✅ Display access URLs

**Time: ~2-3 minutes**

---

## 📋 Method 2: Manual Deployment

If you prefer manual control:

```bash
# Set environment
export GCS_BUCKET="regal-scholar-453620-r7-podcast-storage"
export GCS_PATH="glmp-v2"

# Navigate to glmp-v2 directory
cd glmp-v2

# Deploy viewer
gsutil -m cp -r viewer/* gs://${GCS_BUCKET}/${GCS_PATH}/viewer/

# Deploy processes
gsutil -m cp -r processes/* gs://${GCS_BUCKET}/${GCS_PATH}/processes/

# Deploy data
gsutil -m cp -r data/* gs://${GCS_BUCKET}/${GCS_PATH}/data/

# Deploy README
gsutil cp README.md gs://${GCS_BUCKET}/${GCS_PATH}/README.md

# Make public
gsutil -m acl ch -r -u AllUsers:R gs://${GCS_BUCKET}/${GCS_PATH}/viewer/
gsutil -m acl ch -r -u AllUsers:R gs://${GCS_BUCKET}/${GCS_PATH}/processes/
gsutil -m acl ch -r -u AllUsers:R gs://${GCS_BUCKET}/${GCS_PATH}/data/
gsutil acl ch -u AllUsers:R gs://${GCS_BUCKET}/${GCS_PATH}/README.md

# Set cache headers
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.html
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.js
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.css
```

---

## 🌐 Method 3: Google Cloud Console (No CLI needed)

### Step 1: Download Files

If the files aren't on your local machine:

1. Go to: https://github.com/garywelz/glmp/tree/clean-slate-v2-viewer-system
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Navigate to the `glmp-v2` folder

### Step 2: Upload via Console

1. Go to: https://console.cloud.google.com/storage/browser/regal-scholar-453620-r7-podcast-storage
2. Click "Create folder" → Name it `glmp-v2`
3. Open the `glmp-v2` folder
4. Click "Upload folder" and select:
   - `viewer` folder
   - `processes` folder
   - `data` folder
5. Click "Upload files" and select `README.md`

### Step 3: Make Public

1. Select all uploaded files/folders
2. Click "Permissions" tab
3. Click "Add entry"
4. Entity: `allUsers`
5. Name: `allUsers`
6. Access: `Reader`
7. Click "Save"

---

## ✅ After Deployment - Verify

### Test These URLs

**Main Viewer:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
```

**Individual Processes:**
```
Lac Operon:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_lac_operon

DNA Replication:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_dna_replication_initiation

Transcription:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_transcription_regulation

Cell Cycle:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=yeast_cell_cycle_control
```

**Verify:**
- ✅ Viewer loads with home screen
- ✅ "Browse Processes" shows 4 processes
- ✅ Clicking a process loads the flowchart
- ✅ Citations display with PubMed links
- ✅ Mermaid diagrams render correctly

---

## 🔧 Troubleshooting

### "Permission Denied" Error

**Solution:** Make sure you're authenticated with an account that has write access:

```bash
# Check current account
gcloud auth list

# Re-authenticate if needed
gcloud auth login
# OR
gcloud auth activate-service-account --key-file=YOUR_KEY.json
```

### "Command not found: gcloud"

**Solution:** Install Google Cloud SDK:
- **Mac:** `brew install google-cloud-sdk`
- **Linux:** https://cloud.google.com/sdk/docs/install
- **Windows:** https://cloud.google.com/sdk/docs/install

### "Files not found" Error

**Solution:** Make sure you're in the `glmp-v2` directory:

```bash
cd glmp-v2
ls  # Should show: viewer/ processes/ data/ README.md
```

### Viewer Loads but Processes Don't

**Solution:** Check if processes folder is public:

```bash
gsutil ls -L gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/ecoli_lac_operon.json
```

If not public, set permissions:

```bash
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/
```

---

## 📊 What Gets Deployed

```
gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/
├── viewer/
│   ├── index.html (7.5 KB)
│   ├── viewer.js (9.7 KB)
│   └── styles.css (9.3 KB)
├── processes/
│   ├── ecoli/
│   │   ├── ecoli_lac_operon.json (3.8 KB)
│   │   ├── ecoli_dna_replication_initiation.json (4.7 KB)
│   │   └── ecoli_transcription_regulation.json (4.5 KB)
│   └── yeast/
│       └── yeast_cell_cycle_control.json (5.1 KB)
├── data/
│   └── metadata.json (2.1 KB)
└── README.md (3.4 KB)

Total: ~45 KB
```

---

## 🎯 Next Steps After Deployment

1. **Test all process links** to ensure they work
2. **Share the main URL** with colleagues for feedback
3. **Monitor usage** (optional: set up GCS analytics)
4. **Add more processes** incrementally
5. **Consider custom domain** (optional): `viewer.glmp.org`

---

## 💰 Costs

**Google Cloud Storage costs:**
- Storage: $0.02/GB/month → ~$0.001/month for 45 KB
- Bandwidth: $0.12/GB for first 1TB → ~$0.12 for ~1,000 views
- Operations: Minimal

**Expected monthly cost:** < $1 for moderate usage

---

## 🔗 Sharing Your Work

Once deployed, you can share:

**Short link to main viewer:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
```

**Direct process links** (see verification section above)

**For academic citation:**
```
Welz, G. (2025). GLMP v2: Genome Logic Modeling Project. 
Process: [Name]. Retrieved from [URL].
```

---

## ✨ Success Criteria

Your deployment is successful when:
- ✅ Main viewer loads and shows 4 processes
- ✅ Each process displays its flowchart
- ✅ Citations show with clickable PubMed links
- ✅ All URLs are publicly accessible
- ✅ Mobile-responsive design works

---

**Ready to deploy? Use Method 1 (deployment script) for the easiest experience!**
