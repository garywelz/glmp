# 🚀 Deploy 6 New Processes to GCS

**Status:** Committed to GitHub, need to deploy to GCS  
**Current GCS:** 58 processes  
**After Deploy:** 64 processes

---

## 📦 The 6 New Processes

All in `/workspace/gcs-processes/ecoli/`:

1. **ecoli_dna_replication_elongation.json** (68 nodes, 7 gates, 4 citations)
2. **ecoli_dna_replication_termination.json** (62 nodes, 7 gates, 4 citations)
3. **ecoli_base_excision_repair.json** (71 nodes, 9 gates, 4 citations)
4. **ecoli_nucleotide_excision_repair.json** (74 nodes, 9 gates, 4 citations)
5. **ecoli_mismatch_repair.json** (76 nodes, 11 gates, 4 citations, Nobel Prize)
6. **ecoli_translation_initiation.json** (69 nodes, 9 gates, 4 citations, Nobel Prize)

---

## 🚀 Deploy from Desktop

### **Option 1: Deploy Individual Files (Recommended)**

From your desktop at `/home/gdubs/glmp`:

```bash
# Pull latest from GitHub (has the 6 new files)
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90

# Upload the 6 new processes
gsutil cp glmp-v2/processes/ecoli/ecoli_dna_replication_elongation.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp glmp-v2/processes/ecoli/ecoli_dna_replication_termination.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp glmp-v2/processes/ecoli/ecoli_base_excision_repair.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp glmp-v2/processes/ecoli/ecoli_nucleotide_excision_repair.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp glmp-v2/processes/ecoli/ecoli_mismatch_repair.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/

gsutil cp glmp-v2/processes/ecoli/ecoli_translation_initiation.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/ecoli/
```

### **Option 2: Batch Upload (if you have all 64)**

If your `v2-development` directory has all 64 processes:

```bash
cd /home/gdubs/glmp

# Sync entire processes directory
gsutil -m rsync -r v2-development/processes/ \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/
```

---

## 📊 Update Metadata

The metadata.json also needs updating to show 64 processes.

**Create this file:** `update_metadata_count.py`

```python
import json

# Load metadata
with open('glmp-v2/data/metadata.json', 'r') as f:
    metadata = json.load(f)

# Update counts
metadata['totalProcesses'] = 64
metadata['lastUpdated'] = '2025-10-16'

# Find E. coli in organisms
for org in metadata.get('organisms', []):
    if org['name'] == 'E. coli':
        org['processCount'] = 23  # Was 17, now 23

# Save
with open('glmp-v2/data/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Updated metadata.json to 64 processes")
```

**Run it:**
```bash
python3 update_metadata_count.py

# Upload updated metadata
gsutil cp glmp-v2/data/metadata.json \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/data/metadata.json
```

---

## 🧪 Verify After Deployment

### **Test 1: Check Viewer**
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html

Should show **64 processes** (was 58)

### **Test 2: Check Database Table**
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html

Should show **64 processes** (was 58)

### **Test 3: Test a New Process**
Try loading one of the new ones:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/?process=ecoli_dna_replication_elongation

Should show the flowchart!

---

## ✅ Deployment Checklist

- [ ] Pull latest from GitHub
- [ ] Upload 6 new process files to GCS
- [ ] Update metadata.json count to 64
- [ ] Upload metadata.json to GCS
- [ ] Hard refresh viewer (Ctrl+Shift+R)
- [ ] Verify 64 processes show
- [ ] Test clicking a new process
- [ ] Confirm flowchart loads

---

**After deployment, you'll have 64/100 processes (64% to publication goal)!** 🎯

