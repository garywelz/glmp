# Instructions for Desktop Cursor - Deploy GLMP to GCS

## Overview
You need to upload the `biological_processes` folder from the GitHub repo to Google Cloud Storage to replace old broken files with new fixed ones.

---

## Step-by-Step Instructions

### **Step 1: Open Cursor Terminal**

In Cursor:
- **Mac:** Press `Ctrl + `` (backtick)
- **Windows/Linux:** Press `Ctrl + `` (backtick)
- **Or:** Menu → Terminal → New Terminal

---

### **Step 2: Navigate to Your Cloned Repository**

In the terminal, navigate to where you cloned the repo:

```bash
cd ~/Documents/glmp
```

**Adjust the path** if you cloned it somewhere else. To find it:
```bash
# If you're not sure where it is, search:
find ~ -name "glmp" -type d 2>/dev/null | grep -v node_modules
```

---

### **Step 3: Verify You Have the Files**

Check that the `biological_processes` folder exists:

```bash
ls biological_processes/
```

You should see:
```
ecoli/  yeast/  scripts/  templates/  index.html  logical_analysis_results.json
```

---

### **Step 4: Authenticate with Your Service Account**

Replace `/path/to/your-service-account-key.json` with the actual path to your service account JSON key file:

```bash
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json
```

**Example paths:**
- Mac: `~/Downloads/regal-scholar-service-account.json`
- Windows: `C:\Users\YourName\Downloads\regal-scholar-service-account.json`

Then set the project:

```bash
gcloud config set project regal-scholar-453620-r7
```

---

### **Step 5: Upload Files to Google Cloud Storage**

This command uploads the entire `biological_processes` folder and **overwrites** the old broken files:

```bash
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
```

**What this does:**
- `-m` = parallel upload (faster)
- `-r` = recursive (includes all subfolders)
- Overwrites existing files in GCS

**Expected output:**
```
Copying file://biological_processes/index.html...
Copying file://biological_processes/ecoli/ecoli_batch01...
...
[42 files uploaded]
```

**Time:** 1-2 minutes

---

### **Step 6: Make Files Publicly Accessible**

Set public read permissions so anyone can view the files:

```bash
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

**What this does:**
- Gives everyone (`AllUsers`) read access (`R`)
- Applied recursively (`-r`) to all files

**Time:** 30 seconds

---

### **Step 7: Verify Deployment**

**Option A: Use curl in terminal**

```bash
curl -I https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
```

You should see `HTTP/2 200` (success)

**Option B: Open in browser**

Open these URLs in your browser:

1. **Main Index:**
   ```
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
   ```

2. **E. coli DNA Replication (the one that had errors):**
   ```
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
   ```

3. **Yeast DNA Replication:**
   ```
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/yeast/yeast_batch01_dna_replication_repair.html
   ```

**What you should see:**
- ✅ Working flowcharts (no "Syntax error in text")
- ✅ Interactive sliders that work
- ✅ Proper diagrams for all processes

---

## Complete Command Sequence (Copy & Paste)

Here's everything in one block. **Update the paths** for your system:

```bash
# Navigate to repo
cd ~/Documents/glmp

# Verify files exist
ls biological_processes/

# Authenticate (UPDATE THIS PATH!)
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json

# Set project
gcloud config set project regal-scholar-453620-r7

# Upload files
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/

# Make public
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/

# Verify
echo "✅ Upload complete! Check these URLs:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html"
```

---

## What You're Uploading

```
biological_processes/
├── index.html                           # Main index page
├── logical_analysis_results.json        # Analysis data
│
├── ecoli/                               # 17 files
│   ├── README.md
│   ├── ecoli_batch01_dna_replication_repair.html
│   ├── ecoli_batch02_cell_division_segregation.html
│   ├── ecoli_batch03_translation_protein_synthesis.html
│   ├── ecoli_batch04_protein_synthesis_quality.html
│   ├── ecoli_batch05_cell_division.html
│   ├── ecoli_batch06_stress_response.html
│   ├── ecoli_batch07_transport_membrane.html
│   ├── ecoli_batch08_motility_chemotaxis.html
│   ├── ecoli_batch09_antibiotic_resistance.html
│   ├── ecoli_batch10_iron_homeostasis.html
│   ├── ecoli_batch11_biofilm_formation.html
│   ├── ecoli_batch12_quorum_sensing.html
│   ├── ecoli_batch13_metabolic_pathways.html
│   ├── ecoli_batch14_gene_regulation.html
│   ├── ecoli_batch15_cellular_communication.html
│   ├── ecoli_lac_operon_beta_galactosidase.html
│   └── ecoli_overview_top_10_processes.html
│
├── yeast/                               # 24 files
│   ├── README.md
│   ├── yeast_batch01_dna_replication_repair.html
│   ├── yeast_batch02_cell_cycle_control.html
│   ├── yeast_batch03_protein_synthesis.html
│   ├── yeast_batch04_signal_transduction.html
│   ├── yeast_batch05_energy_metabolism.html
│   ├── yeast_batch06_lipid_membrane_biology.html
│   ├── yeast_batch07_cell_division.html
│   ├── yeast_batch08_metabolic_regulation.html
│   ├── yeast_batch09_gene_expression.html
│   ├── yeast_batch10_protein_folding.html
│   ├── yeast_batch11_cell_wall_biology.html
│   ├── yeast_batch12_organelle_biology.html
│   ├── yeast_batch13_environmental_adaptation.html
│   ├── yeast_batch14_developmental_processes.html
│   ├── yeast_batch15_quality_control_systems.html
│   ├── yeast_batch16_membrane_transport.html
│   ├── yeast_batch17_cell_communication.html
│   ├── yeast_batch18_developmental_biology.html
│   ├── yeast_batch19_stress_response.html
│   ├── yeast_batch20_aging_senescence.html
│   ├── yeast_batch21_epigenetic_regulation.html
│   ├── yeast_batch22_metabolic_engineering.html
│   └── yeast_batch23_synthetic_biology.html
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

**Total:** 42 files, 2.9 MB

---

## Troubleshooting

### "gcloud: command not found"

Install Google Cloud SDK:
- **Mac:** `brew install google-cloud-sdk`
- **Windows:** Download from https://cloud.google.com/sdk/docs/install
- **Linux:** Follow instructions at https://cloud.google.com/sdk/docs/install

### "Permission denied" or "Access denied"

Check:
1. Service account key file path is correct
2. Service account has "Storage Object Admin" role
3. You're using the right Google Cloud project

### "gsutil: command not found"

Reinstall gcloud or add to PATH:
```bash
export PATH=$PATH:$HOME/google-cloud-sdk/bin
```

### Upload seems stuck

- Press Ctrl+C to cancel
- Try without `-m` flag: `gsutil cp -r ...`
- Check internet connection

### Files upload but still show errors

- Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)
- Wait 1-2 minutes for GCS cache to clear
- Try incognito/private browsing mode

---

## Expected Timeline

| Step | Time |
|------|------|
| Navigate to repo | 10 seconds |
| Authenticate | 30 seconds |
| Upload files | 1-2 minutes |
| Set permissions | 30 seconds |
| Verify | 30 seconds |
| **Total** | **~3-5 minutes** |

---

## Success Criteria

✅ All 42 files uploaded successfully  
✅ No "Syntax error in text" messages in browser  
✅ Flowcharts render correctly  
✅ Interactive sliders work  
✅ All URLs are publicly accessible  

---

## After Successful Upload

The following URLs will have working content:

**Main Pages:**
- Biology Index: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html

**E. coli Processes (15 processes):**
- All files in: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/

**Yeast Processes (23 processes):**
- All files in: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/yeast/

---

## Important Notes

1. **This OVERWRITES old files** - the broken versions will be replaced
2. **No backup needed** - old files had errors, new ones are fixed
3. **Wait 1-2 minutes** after upload before testing (GCS cache)
4. **Keep service account key secure** - don't commit it to git

---

## Quick Reference

**Find your repo:**
```bash
find ~ -name "glmp" -type d 2>/dev/null | head -1
```

**Check if gcloud is installed:**
```bash
gcloud --version
```

**List what's currently in GCS:**
```bash
gsutil ls gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

**Delete old version first (optional):**
```bash
gsutil -m rm -r gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

---

## Summary

1. Open terminal in Cursor
2. Navigate to cloned `glmp` repo
3. Authenticate with service account key
4. Run upload command
5. Set public permissions
6. Verify in browser

**That's it! The fixed files will replace the broken ones in GCS.**

---

**Questions?** Check the troubleshooting section above or refer to `/workspace/DEPLOY_WITH_SERVICE_ACCOUNT.md` for more details.
