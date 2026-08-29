# How to Get Files from Remote Workspace to Upload to GCS

## The Problem
The files are on this remote workspace machine (`/workspace/biological_processes/`), not on your local computer or in GCS yet. The links aren't clickable because they're file paths, not URLs.

## ✅ 3 EASY SOLUTIONS

---

### **OPTION 1: Download from GitHub (EASIEST!)** ⭐

The files are already in your GitHub repository!

**Steps:**

1. **Clone the repo to your local machine:**
   ```bash
   git clone https://github.com/garywelz/glmp.git
   cd glmp
   ```

2. **The `biological_processes` folder is already there!**
   ```bash
   ls biological_processes/
   # You'll see: ecoli/ yeast/ scripts/ templates/ index.html
   ```

3. **Deploy to GCS:**
   ```bash
   # Authenticate with your service account
   gcloud auth activate-service-account --key-file=/path/to/your-key.json
   
   # Set project
   gcloud config set project regal-scholar-453620-r7
   
   # Upload to GCS
   gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
   
   # Make public
   gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
   ```

**Time: ~5 minutes** (if you already have git and gcloud)

---

### **OPTION 2: Download Archive Files**

I've created compressed archives for you:

**Available archives:**
- `/workspace/biological_processes.tar.gz` (194 KB)
- `/workspace/biological_processes.zip` (244 KB)

**How to download:**

If you have terminal/SSH access to this workspace:

```bash
# From your local machine, use scp to download:
scp user@workspace-host:/workspace/biological_processes.tar.gz ~/Downloads/

# Or if using a web-based workspace, use the download feature
```

Then extract and upload:

```bash
# Extract
tar -xzf biological_processes.tar.gz
# OR
unzip biological_processes.zip

# Upload to GCS
gcloud auth activate-service-account --key-file=/path/to/your-key.json
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

---

### **OPTION 3: Push to GitHub and Clone (If files aren't in GitHub yet)**

If the biological_processes folder isn't in GitHub yet:

**From this workspace:**
```bash
cd /workspace
git add biological_processes/
git commit -m "Add standardized biological processes"
git push origin HEAD
```

**Then on your local machine:**
```bash
git clone https://github.com/garywelz/glmp.git
cd glmp
# Deploy as shown in Option 1
```

---

## 🎯 RECOMMENDED: Use Option 1 (GitHub Clone)

**Why?**
- Fastest (files already in GitHub)
- No file transfers needed
- You get the entire project
- Easy to keep updated

**Quick commands:**
```bash
# On your local machine
git clone https://github.com/garywelz/glmp.git
cd glmp
gcloud auth activate-service-account --key-file=YOUR-KEY.json
gcloud config set project regal-scholar-453620-r7
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

---

## 🔗 After Upload - Verify These URLs Work

Once uploaded, these URLs should work:

**Main Index:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
```

**E. coli Sample:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
```

**Yeast Sample:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/yeast/yeast_batch01_dna_replication_repair.html
```

---

## 📊 What's in the Files

```
biological_processes/
├── index.html                           # Main index page
├── logical_analysis_results.json        # Analysis data
│
├── ecoli/                               # 17 files
│   ├── README.md
│   ├── ecoli_batch01_dna_replication_repair.html
│   ├── ... (13 more batch files)
│   ├── ecoli_lac_operon_beta_galactosidase.html
│   └── ecoli_overview_top_10_processes.html
│
├── yeast/                               # 24 files
│   ├── README.md
│   └── yeast_batch01-23_*.html
│
├── scripts/                             # 5 files
│   ├── create_yeast_batches.py
│   ├── database_schema_with_logic.sql
│   ├── generate_database_entries.py
│   ├── logical_structure_analyzer.py
│   └── simple_logic_analysis.py
│
└── templates/
    └── biological_process_template.html
```

**Total:** 42 files, 2.9 MB uncompressed

---

## ✅ Complete Workflow

1. **Get files** (Option 1 - GitHub clone)
2. **Authenticate** with service account
3. **Upload** to GCS with gsutil
4. **Make public** with acl command
5. **Verify** URLs work

**Total time: 5-10 minutes**

---

## 💡 Quick Summary

**The files exist in:**
- ✅ This remote workspace: `/workspace/biological_processes/`
- ✅ GitHub repo: `https://github.com/garywelz/glmp`
- ✅ Compressed archives: `biological_processes.tar.gz` and `.zip`
- ❌ NOT in GCS yet (that's what you need to do)

**Easiest method:** Clone from GitHub and upload to GCS using the commands in Option 1.
