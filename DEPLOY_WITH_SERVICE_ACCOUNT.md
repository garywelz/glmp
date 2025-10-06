# Deploy GLMP with Your Service Account

## ✅ You Have Everything You Need!

- ✅ Service account in `regal-scholar-453620-r7`
- ✅ gcloud CLI installed
- ✅ Files ready in `/workspace/biological_processes/`

## 📁 File Location

The `biological_processes` folder is located at:

```
/workspace/biological_processes/
```

**Size:** 2.9 MB  
**Contents:**
- 39 HTML files (15 E. coli + 23 yeast + 1 index)
- 5 Python scripts
- 1 template file
- 1 JSON analysis file
- 2 README files

## 🚀 Quick Deploy Commands

### Option 1: If Files Are Already on Your Local Machine

If you have access to the `/workspace/` directory on your computer:

```bash
# 1. Authenticate with your service account
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json

# 2. Set the project
gcloud config set project regal-scholar-453620-r7

# 3. Deploy the folder
gsutil -m cp -r /workspace/biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/

# 4. Set public permissions
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/

# 5. Verify deployment
gsutil ls gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

### Option 2: If You Need to Download Files First

If you're on a different machine and need to get the files:

```bash
# If the workspace is in a git repo, clone it:
git clone https://github.com/garywelz/glmp.git
cd glmp

# Then authenticate and deploy:
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json
gcloud config set project regal-scholar-453620-r7
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

### Option 3: Deploy from This Workspace (If You're Here)

If you have SSH or terminal access to this workspace:

```bash
# Navigate to workspace
cd /workspace

# Authenticate with service account
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json

# Set project
gcloud config set project regal-scholar-453620-r7

# Deploy
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/

# Set permissions
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

## 📂 What's in biological_processes/

```
biological_processes/
├── index.html                           (Main index page)
├── logical_analysis_results.json        (Analysis data)
│
├── ecoli/                               (15 HTML files)
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
├── yeast/                               (23 HTML files)
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
├── scripts/                             (5 Python files)
│   ├── create_yeast_batches.py
│   ├── database_schema_with_logic.sql
│   ├── generate_database_entries.py
│   ├── logical_structure_analyzer.py
│   └── simple_logic_analysis.py
│
└── templates/
    └── biological_process_template.html
```

## 🔗 After Deployment - View URLs

Once deployed, your files will be accessible at:

**Main Index:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
```

**E. coli Processes:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
```

**Yeast Processes:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/yeast/yeast_batch01_dna_replication_repair.html
```

## ✅ Verification Commands

After deployment, verify with:

```bash
# List deployed files
gsutil ls gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/

# Check a specific file
gsutil ls gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html

# Test public access (should return 200)
curl -I https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
```

## 🔐 Service Account Authentication

Your service account key file is typically a JSON file that looks like:

```json
{
  "type": "service_account",
  "project_id": "regal-scholar-453620-r7",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  ...
}
```

To use it:
```bash
gcloud auth activate-service-account --key-file=/path/to/key.json
```

## ⏱️ Deployment Time

- **Authentication:** 30 seconds
- **Upload (2.9 MB):** 1-2 minutes
- **Set permissions:** 30 seconds
- **Verification:** 30 seconds

**Total: ~3-5 minutes**

## 🆘 Troubleshooting

**Error: "Permission denied"**
```bash
# Make sure service account has Storage Object Admin role
gcloud projects add-iam-policy-binding regal-scholar-453620-r7 \
  --member="serviceAccount:YOUR-SERVICE-ACCOUNT@regal-scholar-453620-r7.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

**Error: "Cannot find workspace folder"**
- If you're on a different machine, you need to download/clone the files first
- Or use the Google Cloud Console web upload method

**Error: "gsutil: command not found"**
```bash
# Reinstall gcloud SDK or update PATH
export PATH=$PATH:$HOME/google-cloud-sdk/bin
```

## 🎯 Summary

**You need to:**
1. Find your service account JSON key file
2. Run `gcloud auth activate-service-account --key-file=YOUR-KEY.json`
3. Run `gsutil -m cp -r /workspace/biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/`
4. Run `gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/`

**Done! Takes ~3-5 minutes.**
