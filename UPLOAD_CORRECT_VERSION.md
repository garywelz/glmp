# Upload the Correct Version to GCS

## ⚠️ You Found an Old Version in GCS!

The file currently at:
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
```

Has **Mermaid syntax errors** - this is an OLD version.

## ✅ The NEW, Fixed Version is in Your Cloned Repo

The corrected files are in the GitHub repo you just cloned.

---

## 🚀 What to Do Next - Upload the Correct Files

### **Step 1: Navigate to Your Cloned Repo**

In Cursor's terminal:
```bash
cd ~/path/to/glmp  # wherever you cloned it
```

### **Step 2: Verify You Have the New Files**

```bash
ls biological_processes/ecoli/ | head -5
# Should show files like:
# ecoli_batch01_dna_replication_repair.html
# ecoli_batch02_cell_division_segregation.html
# etc.
```

### **Step 3: Authenticate with Your Service Account**

```bash
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json
gcloud config set project regal-scholar-453620-r7
```

### **Step 4: Upload the ENTIRE biological_processes Folder**

This will **replace** the old broken files with the new working ones:

```bash
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
```

**Note:** The `-m` flag enables parallel uploads (faster)

### **Step 5: Make Files Publicly Accessible**

```bash
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

### **Step 6: Verify the Fix**

Wait a minute for the cache to clear, then reload:
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
```

You should now see working flowcharts instead of "Syntax error in text"!

---

## 📊 What's Different in the New Version

**Old version (currently in GCS):**
- ❌ Mermaid syntax errors
- ❌ Shows "Syntax error in text" for all diagrams
- ❌ Created by an earlier agent with bugs

**New version (in GitHub repo):**
- ✅ Fixed Mermaid syntax
- ✅ Working interactive flowcharts
- ✅ Created by "Standardize Yeast Biology charts" agent
- ✅ 130+ files updated/created
- ✅ Proper error-free rendering

---

## 🎯 Complete Command Sequence

Just copy and paste these commands (update paths as needed):

```bash
# 1. Navigate to your cloned repo
cd ~/Documents/glmp  # or wherever you cloned it

# 2. Authenticate
gcloud auth activate-service-account --key-file=/path/to/your-key.json
gcloud config set project regal-scholar-453620-r7

# 3. Upload (this overwrites old files)
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/

# 4. Set public access
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/

# 5. Verify
echo "✅ Upload complete! Check these URLs:"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html"
echo "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html"
```

---

## ⏱️ Expected Time

- Authentication: 30 seconds
- Upload 42 files (2.9 MB): 1-2 minutes
- Set permissions: 30 seconds
- **Total: ~3 minutes**

---

## ✅ How to Verify It Worked

After uploading, check:

1. **No more "Syntax error in text"** - diagrams should render
2. **Interactive sliders work** - you can change detail levels
3. **All 8 processes show flowcharts** - not error messages

---

## 🔍 Why This Happened

The `biological_processes` folder in GCS is from an **earlier version** before the standardization work was completed. The new files in GitHub were created by the "Standardize Yeast Biology charts" agent with all syntax errors fixed.

By uploading from your cloned repo, you're **replacing** the broken old files with the corrected new ones.

---

## 📝 Summary

**Current state:**
- ❌ GCS has old broken files
- ✅ GitHub has new working files
- ✅ You cloned GitHub to your computer

**What to do:**
1. ✅ Run the upload commands above
2. ✅ This overwrites old files with new ones
3. ✅ Verify the URLs work correctly

**Result:** Working flowcharts with no syntax errors!

---

Ready to upload? Just run the commands in the "Complete Command Sequence" section above!
