# 🚀 Hugging Face Upload Guide

## ✅ Files Ready for Upload

Your biological process flowcharts are now properly organized:
- **21 E. coli files** in `processes/ecoli/`
- **23 Yeast files** in `processes/yeast/`
- **Total: 44 files** ready for upload

## 📁 Upload Options

### Option 1: Direct Git Push to Hugging Face (Recommended)

If your Hugging Face space supports git (which most do), you can add it as a remote:

```bash
# Add Hugging Face space as a remote
git remote add huggingface https://huggingface.co/spaces/garywelz/glmp

# Add the new files
git add processes/

# Commit the files
git commit -m "Add standardized biological process flowcharts

- 21 E. coli batch files with 5-level interactive sliders
- 23 yeast batch files with 5-level interactive sliders
- Universal color scheme applied (Red, Yellow, Green, Blue, Violet)
- Fixed Mermaid syntax formatting
- Diamond shapes for logic gates
- Anchor tags for direct process linking
- Total: 352 biological processes with 1,760 interactive diagrams"

# Push to Hugging Face
git push huggingface main
```

### Option 2: Hugging Face Web Interface

1. **Navigate to your space**: https://huggingface.co/spaces/garywelz/glmp
2. **Click "Files" tab**
3. **Create folder structure**:
   - Click "Add file" → "Create folder" → Name: `processes`
   - Inside `processes`, create `ecoli` and `yeast` folders
4. **Upload files**:
   - Navigate to `processes/ecoli/`
   - Click "Add file" → "Upload files"
   - Select all 21 E. coli files from your `processes/ecoli/` directory
   - Repeat for `processes/yeast/` with all 23 yeast files

### Option 3: Hugging Face Hub CLI

If you have the Hugging Face CLI installed:

```bash
# Install if needed
pip install huggingface_hub

# Login (if not already logged in)
huggingface-cli login

# Upload the entire processes directory
huggingface-cli upload garywelz/glmp processes/ processes/ --repo-type space
```

### Option 4: Python Script Upload

```python
from huggingface_hub import HfApi
import os

api = HfApi()

# Upload E. coli files
ecoli_files = os.listdir('processes/ecoli/')
for file in ecoli_files:
    api.upload_file(
        path_or_fileobj=f'processes/ecoli/{file}',
        path_in_repo=f'processes/ecoli/{file}',
        repo_id='garywelz/glmp',
        repo_type='space'
    )

# Upload yeast files  
yeast_files = os.listdir('processes/yeast/')
for file in yeast_files:
    api.upload_file(
        path_or_fileobj=f'processes/yeast/{file}',
        path_in_repo=f'processes/yeast/{file}',
        repo_id='garywelz/glmp',
        repo_type='space'
    )
```

## 🎯 Recommended Approach

**I recommend Option 1 (Git Push)** because:
- ✅ Fastest for bulk uploads
- ✅ Maintains version history
- ✅ Single command uploads all files
- ✅ Atomic operation (all files uploaded together)

## 🌐 Final URLs After Upload

Once uploaded, your files will be accessible at:

**E. coli URLs**:
- `https://garywelz-glmp.static.hf.space/processes/ecoli/ecoli_batch01_dna_replication_repair.html`
- `https://garywelz-glmp.static.hf.space/processes/ecoli/ecoli_batch02_cell_division_segregation.html`
- ... (all 21 files)

**Yeast URLs**:
- `https://garywelz-glmp.static.hf.space/processes/yeast/yeast_batch01_dna_replication_repair.html`
- `https://garywelz-glmp.static.hf.space/processes/yeast/yeast_batch02_cell_cycle_control.html`
- ... (all 23 files)

**Direct Process Linking**:
- Add `#process-[1-8]` to any URL for direct process navigation
- Example: `https://garywelz-glmp.static.hf.space/processes/ecoli/ecoli_batch01_dna_replication_repair.html#process-3`

## ⚡ Quick Start Commands

```bash
# Navigate to your workspace
cd /workspace

# Add Hugging Face remote and push (Option 1)
git remote add huggingface https://huggingface.co/spaces/garywelz/glmp
git add processes/
git commit -m "Add standardized biological process flowcharts - 44 files with 352 processes"
git push huggingface main
```

## 🔍 Verification

After upload, test a few URLs to ensure everything works:
1. Check that files are accessible
2. Verify sliders work properly  
3. Test anchor links with `#process-[number]`
4. Confirm Mermaid diagrams render correctly

---

**Status**: Ready for upload using any of the 4 methods above  
**Recommendation**: Use Option 1 (Git Push) for fastest bulk upload