# 🔍 Check Which Yeast Files Are Most Current

## 📁 **Your Local Files**
Location: `/home/gdubs/glmp/collections/yeast/` (23 files)

## 📁 **Today's Standardized Files** 
Location: `/workspace/processes/yeast/` (23 files)

## 🔍 **How to Check Which Are More Current**

### **Method 1: Check File Timestamps**

In your WSL terminal, run:

```bash
# Check timestamps of your local collections files
ls -la /home/gdubs/glmp/collections/yeast/ | head -10

# Check if your files are from yesterday or today
stat /home/gdubs/glmp/collections/yeast/yeast_batch01_dna_replication_repair.html | grep Modify
```

### **Method 2: Check File Sizes**

```bash
# Check file sizes of your local files
ls -lh /home/gdubs/glmp/collections/yeast/ | head -5

# Compare with expected sizes (today's files are typically 20-80KB each)
```

### **Method 3: Check Standardization Features**

Open one of your local yeast files and check for:

```bash
# Check if your local files have standardization features
grep -c "allProcesses\|fill:#ff6b6b" /home/gdubs/glmp/collections/yeast/yeast_batch01_dna_replication_repair.html
```

**Expected results for standardized files:**
- Should find `allProcesses` (interactive sliders)
- Should find `fill:#ff6b6b` (universal colors)

## 🎯 **Decision Guide**

### **Use Your Local Files IF:**
- ✅ Timestamps show they're from today (Sep 12, 2025)
- ✅ File sizes are reasonable (20-80KB each)
- ✅ They contain `allProcesses` and universal colors

### **Use Today's Cloud Files IF:**
- ❌ Your local files are from yesterday (Sep 11, 2025)
- ❌ They're missing standardization features
- ❌ File sizes seem too small or inconsistent

## 🚀 **Commands to Use**

### **If Your Local Files Are Current:**
```bash
# Copy your local collections files to deployment directory
cp /home/gdubs/glmp/collections/yeast/* /home/gdubs/glmp/glmp-deployment/processes/yeast/

# Verify
ls /home/gdubs/glmp/glmp-deployment/processes/yeast/ | wc -l  # Should be 23
```

### **If Cloud Files Are More Current:**
```bash
# Copy from cloud workspace (if accessible)
cp /workspace/processes/yeast/* /home/gdubs/glmp/glmp-deployment/processes/yeast/

# Or download the archive first, then extract
```

## 📊 **Quick Test Commands**

Run these in your WSL terminal to help decide:

```bash
echo "=== LOCAL COLLECTIONS YEAST FILES ==="
ls -la /home/gdubs/glmp/collections/yeast/ | head -3
echo "File count: $(ls /home/gdubs/glmp/collections/yeast/ | wc -l)"

echo -e "\n=== CHECKING STANDARDIZATION ==="
grep -c "allProcesses" /home/gdubs/glmp/collections/yeast/yeast_batch01_dna_replication_repair.html 2>/dev/null || echo "File not found or no allProcesses"

grep -c "fill:#ff6b6b" /home/gdubs/glmp/collections/yeast/yeast_batch01_dna_replication_repair.html 2>/dev/null || echo "No universal colors found"
```

---

**Run the test commands above and let me know the results - then I can tell you definitively which files to use!** 🎯