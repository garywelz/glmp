# 🚀 Deploy GLMP v2 to GCS - Complete Guide

**Quick Start:** Just run `./DEPLOY_TO_GCS.sh` after authentication!

---

## What You're Deploying

✅ **GLMP v2 - Clean Slate Viewer System**
- 4 gold-standard biological processes
- 18 verified citations (Nobel Prize papers included!)
- Individual process files (modular architecture)
- Beautiful responsive viewer
- Publication-ready quality

---

## Prerequisites

You need:
1. ✅ Google Cloud SDK installed (`gcloud` and `gsutil`)
2. ✅ Access to service account key for `regal-scholar-453620-r7` project
3. ✅ The glmp-v2 files (from GitHub)

---

## 🎯 Deployment Steps (3 Minutes)

### Step 1: Get the Files

**On your local machine (in terminal):**

```bash
# Clone the repo
git clone https://github.com/garywelz/glmp.git
cd glmp

# Switch to the clean-slate branch
git checkout clean-slate-v2-viewer-system

# Navigate to v2 directory
cd glmp-v2

# Verify files exist
ls
# Should see: viewer/ processes/ data/ README.md DEPLOY_TO_GCS.sh
```

### Step 2: Authenticate

```bash
# Using service account
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json

# Set project
gcloud config set project regal-scholar-453620-r7
```

### Step 3: Deploy!

```bash
# Run the deployment script
./DEPLOY_TO_GCS.sh
```

**That's it!** The script handles everything.

---

## 📋 What the Script Does

The automated script will:

1. ✅ Verify authentication
2. ✅ Check bucket access
3. ✅ Upload viewer files (HTML, JS, CSS)
4. ✅ Upload process files (4 JSON files)
5. ✅ Upload data files (metadata.json)
6. ✅ Upload README
7. ✅ Set public read permissions
8. ✅ Configure cache headers
9. ✅ Display all access URLs

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║     GLMP v2 - Google Cloud Storage Deployment            ║
╚══════════════════════════════════════════════════════════╝

✓ Authenticated as: your-account@...
✓ Project set to: regal-scholar-453620-r7
✓ Bucket accessible

[1/4] Deploying viewer...
✓ Viewer deployed

[2/4] Deploying processes...
✓ Processes deployed (4 files)

[3/4] Deploying data files...
✓ Data files deployed

[4/4] Setting public access permissions...
✓ Public access configured

╔══════════════════════════════════════════════════════════╗
║              ✓ Deployment Complete!                      ║
╚══════════════════════════════════════════════════════════╝

Your GLMP v2 Viewer is now live at:
https://storage.googleapis.com/...
```

---

## 🔗 Your Live URLs (After Deployment)

### Main Viewer
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
```

### Direct Process Links

**Lac Operon (Nobel Prize winning work):**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_lac_operon
```

**DNA Replication Initiation:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_dna_replication_initiation
```

**Transcription Regulation:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_transcription_regulation
```

**Yeast Cell Cycle Control:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=yeast_cell_cycle_control
```

---

## ✅ Verification Checklist

After deployment, test these:

- [ ] Main viewer loads with home screen
- [ ] "Browse Processes" button shows 4 processes
- [ ] E. coli section shows 3 processes
- [ ] Yeast section shows 1 process
- [ ] Clicking "Lac Operon" loads the process
- [ ] Flowchart renders correctly (no "Syntax error")
- [ ] Citations section shows 4 sources with PubMed links
- [ ] PubMed links are clickable and work
- [ ] Back button returns to process list
- [ ] All 4 processes load correctly
- [ ] Mobile view is responsive (test on phone)

---

## 🔧 If You Need Manual Deployment

If the script doesn't work for some reason:

```bash
# After authentication (steps 1-2 above)
cd glmp-v2

# Deploy files
gsutil -m cp -r viewer/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
gsutil -m cp -r processes/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/
gsutil -m cp -r data/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/
gsutil cp README.md gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/README.md

# Make public
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/

# Set cache (optional)
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/*.html
```

---

## 🎯 Expected Timeline

| Step | Time |
|------|------|
| Clone repo | 30 sec |
| Authenticate | 30 sec |
| Run script | 2 min |
| Verify | 1 min |
| **Total** | **4 minutes** |

---

## 🌟 What You Get

After deployment, you'll have:

### A Professional Biological Process Viewer
- ✅ Clean, modern interface
- ✅ Responsive design (works on all devices)
- ✅ Fast loading (45 KB total)
- ✅ Globally distributed (GCS CDN)

### 4 Publication-Quality Processes
- ✅ Each with 4-5 verified citations
- ✅ PubMed IDs and DOIs
- ✅ Interactive Mermaid diagrams
- ✅ Complete metadata

### Ready to Share
- ✅ Public URLs
- ✅ Direct process linking
- ✅ Academic citation format
- ✅ Professional presentation

---

## 💰 Cost

**Google Cloud Storage:**
- Storage: ~$0.001/month (45 KB)
- Bandwidth: ~$0.12/GB transferred
- Operations: Minimal

**Expected cost:** Less than $1/month for moderate usage

---

## 🔄 Adding More Processes Later

After initial deployment, adding new processes is easy:

```bash
# Create new process JSON file locally
# Test in viewer
# Then deploy just that file:

gsutil cp processes/ecoli/new_process.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil acl ch -u AllUsers:R \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/new_process.json

# Update metadata.json
gsutil cp data/metadata.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/
```

---

## 📱 Sharing Your Work

Once deployed, share:

**Main viewer:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
```

**Specific process:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/?process=ecoli_lac_operon
```

**For academic citation:**
```
Welz, G. (2025). GLMP v2: Genome Logic Modeling Project.
Lac Operon Regulation. Retrieved from [URL].
```

---

## 🆘 Troubleshooting

### Issue: "Permission denied"

**Solution:**
```bash
# Make sure you're using the right account
gcloud auth list

# Re-authenticate
gcloud auth activate-service-account --key-file=YOUR_KEY.json
```

### Issue: "Script permission denied"

**Solution:**
```bash
chmod +x DEPLOY_TO_GCS.sh
```

### Issue: "Files not found"

**Solution:**
```bash
# Make sure you're in glmp-v2 directory
pwd  # Should end with /glmp-v2

# Check branch
git branch  # Should show * clean-slate-v2-viewer-system
```

### Issue: Deployed but viewer doesn't load

**Solution:**
1. Clear browser cache (Cmd/Ctrl + Shift + R)
2. Wait 1-2 minutes for GCS cache to clear
3. Try incognito/private mode
4. Check browser console for errors

---

## ✨ Success!

Once deployed, you'll see:
- ✅ Beautiful viewer interface
- ✅ 4 processes in catalog
- ✅ Working flowcharts (no errors!)
- ✅ Clickable PubMed citations
- ✅ Professional presentation

**Ready to share with the scientific community!**

---

## 🎓 Next Steps After Deployment

1. **Test all URLs** - verify everything works
2. **Share with colleagues** - get feedback
3. **Add more processes** - grow the collection
4. **Consider custom domain** - e.g., viewer.glmp.org
5. **Track usage** - optional GCS analytics
6. **Plan publication** - academic paper or preprint

---

**Ready to deploy? Run the commands in Step 1-3 and you'll be live in 3 minutes!**

For complete details, see `DEPLOYMENT_INSTRUCTIONS.md` in the glmp-v2 folder.
