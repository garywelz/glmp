# 🔄 Transfer Latest Files to WSL Ubuntu Directory

## 📂 **Target Location**
Your WSL directory: `/home/gdubs/glmp/glmp-deployment/processes/`

## 🚀 **Method 1: Direct File Copy (Recommended)**

If you can access the cloud workspace files from your Windows system:

### **Step 1: Copy from Cloud to Windows Desktop**
```bash
# In Windows File Explorer, navigate to the cloud workspace and copy:
# /workspace/glmp_deployment_latest.tar.gz
# Save it to your Windows Desktop
```

### **Step 2: Transfer to WSL Ubuntu**
Open **WSL Ubuntu terminal** and run:

```bash
# Navigate to your Windows Desktop from WSL
cd /mnt/c/Users/YourWindowsUsername/Desktop/

# Copy the archive to your home directory
cp glmp_deployment_latest.tar.gz ~/

# Extract the files
cd ~
tar -xzf glmp_deployment_latest.tar.gz

# Copy to your glmp-deployment directory (backup existing first)
cd /home/gdubs/glmp/glmp-deployment/

# Backup existing files (optional but recommended)
mv processes processes_backup_$(date +%Y%m%d_%H%M%S)

# Copy new standardized files
cp -r ~/transfer_package/glmp-deployment/processes .

# Verify the transfer
ls -la processes/
echo "E. coli files: $(ls processes/ecoli/ | wc -l)"
echo "Yeast files: $(ls processes/yeast/ | wc -l)"
```

## 🚀 **Method 2: Direct WSL Commands (If you have git access)**

If this cloud workspace is accessible via git:

```bash
# In WSL Ubuntu terminal
cd /home/gdubs/glmp/

# Pull latest changes (if this is a git repo)
git pull origin main

# Or clone fresh if needed
# git clone https://github.com/garywelz/glmp.git glmp-new
```

## 🚀 **Method 3: Manual File Copy via Windows Explorer**

1. **Access cloud workspace files** through your file system
2. **Navigate to**: `/workspace/transfer_package/glmp-deployment/processes/`
3. **Copy the entire `processes` folder**
4. **In Windows Explorer, go to**: `\\wsl.localhost\Ubuntu\home\gdubs\glmp\glmp-deployment\`
5. **Backup existing `processes` folder** (rename it to `processes_old`)
6. **Paste the new `processes` folder**

## ✅ **Verification Commands**

After transfer, verify in WSL Ubuntu:

```bash
cd /home/gdubs/glmp/glmp-deployment/

# Check file counts
echo "E. coli files: $(ls processes/ecoli/ | wc -l)"    # Should be 21
echo "Yeast files: $(ls processes/yeast/ | wc -l)"      # Should be 23

# Check a sample file for standardization
head -50 processes/ecoli/ecoli_batch01_dna_replication_repair.html | grep -E "(allProcesses|fill:#ff6b6b)"

# Check file timestamps
ls -la processes/ecoli/ | head -5
```

## 🎯 **Expected Results**

After successful transfer:
- ✅ **21 E. coli files** in `processes/ecoli/`
- ✅ **23 yeast files** in `processes/yeast/`  
- ✅ **All files standardized** with today's improvements
- ✅ **Universal color scheme** applied
- ✅ **Interactive features** where supported

## 🚀 **Next Step: Upload to Hugging Face**

Once files are in your WSL directory:

```bash
cd /home/gdubs/glmp/glmp-deployment/

# Add and commit to git
git add processes/
git commit -m "Update with latest standardized biological process files - 44 files total"

# Push to Hugging Face (if remote is set up)
git push huggingface main
```

---

**Choose the method that works best with your current setup!** Method 1 (file copy via Windows Desktop) is usually the most reliable. 🎯