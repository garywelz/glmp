# 📁 Transfer Missing Yeast Files to Your WSL Directory

## 🎯 **Situation**
- ✅ **E. coli files**: You have all 21 files locally
- ❌ **Yeast files**: You have 0 out of 23 files needed

## 🚀 **Simplest Method: Cursor File Explorer**

### **Step 1: Access Cloud Workspace Files in Cursor**
1. **In Cursor**, navigate to the cloud workspace file explorer
2. **Find the folder**: `/workspace/processes/yeast/`
3. **You should see all 23 yeast files** listed

### **Step 2: Select All Yeast Files**
1. **Select all 23 yeast files** in `/workspace/processes/yeast/`
2. **Copy them** (Ctrl+C)

### **Step 3: Navigate to Your Local WSL Directory**
1. **In Cursor**, navigate to your local WSL directory:
   - Path: `/home/gdubs/glmp/glmp-deployment/processes/yeast/`
2. **Paste the files** (Ctrl+V)

## 📋 **All 23 Yeast Files You Need to Copy**

```
yeast_batch01_dna_replication_repair.html
yeast_batch02_cell_cycle_control.html
yeast_batch03_protein_synthesis_degradation.html
yeast_batch04_signal_transduction.html
yeast_batch05_energy_metabolism.html
yeast_batch06_lipid_membrane_biology.html
yeast_batch07_cell_wall_extracellular.html
yeast_batch08_chromatin_transcription.html
yeast_batch09_rna_processing_transport.html
yeast_batch10_stress_response_adaptation.html
yeast_batch11_advanced_metabolic_pathways.html
yeast_batch12_advanced_regulatory_networks.html
yeast_batch13_environmental_adaptation.html
yeast_batch14_developmental_processes.html
yeast_batch15_quality_control_systems.html
yeast_batch16_membrane_transport.html
yeast_batch17_cell_communication.html
yeast_batch18_developmental_biology.html
yeast_batch19_stress_response.html
yeast_batch20_aging_senescence.html
yeast_batch21_epigenetic_regulation.html
yeast_batch22_metabolic_engineering.html
yeast_batch23_synthetic_biology.html
```

## 🔄 **Alternative: Terminal Commands**

If you can access this cloud workspace from your WSL terminal:

```bash
# Navigate to your local directory
cd /home/gdubs/glmp/glmp-deployment/

# If you have git access to this cloud workspace
git pull origin main

# Or if you can access the cloud files directly
# (replace with actual path to cloud workspace)
cp /path/to/cloud/workspace/processes/yeast/* processes/yeast/
```

## ✅ **Verification**

After copying, verify in your WSL terminal:

```bash
cd /home/gdubs/glmp/glmp-deployment/processes/

# Check counts
echo "E. coli files: $(ls ecoli/ | wc -l)"    # Should be 21
echo "Yeast files: $(ls yeast/ | wc -l)"      # Should be 23

# List yeast files to confirm
ls yeast/ | sort
```

## 🚀 **After You Have All Files**

Once you have all 44 files (21 E. coli + 23 yeast):

```bash
cd /home/gdubs/glmp/glmp-deployment/

# Add to git
git add processes/
git commit -m "Add complete set of standardized biological process files"

# Push to Hugging Face
git push huggingface main
```

---

**Try the Cursor file explorer method first - it's usually the most reliable for copying files between cloud workspace and local WSL directory!** 🎯