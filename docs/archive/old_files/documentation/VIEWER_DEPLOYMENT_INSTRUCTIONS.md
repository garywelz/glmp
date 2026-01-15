# 🚀 GLMP Viewer - Deployment Instructions

**Status:** ✅ Fixed and committed to GitHub  
**Commit:** 805cb41  
**Date:** October 16, 2025

---

## ✅ What Was Fixed

All fixes from Desktop Agent have been applied to `glmp-v2/viewer/viewer.js`:

1. ✅ **Absolute GCS URLs** (was: relative paths `../processes/`)
2. ✅ **Console logging** for debugging
3. ✅ **Navigation button** visibility fix
4. ✅ **Committed to git** and pushed to GitHub

---

## 🚀 Deploy to GCS (Choose One Method)

### **Method 1: Direct Upload (Fastest)**

From your desktop, run:

```bash
cd ~/glmp

# Pull the latest changes from GitHub
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90

# Upload the fixed viewer.js
gsutil cp glmp-v2/viewer/viewer.js \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js

# Verify it uploaded
gsutil ls -l gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js

# Set cache headers (optional - forces browsers to refresh)
gsutil setmeta -h "Cache-Control:public, max-age=300" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js
```

### **Method 2: GCS Console Upload**

1. Go to: https://console.cloud.google.com/storage/browser/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer
2. Click on `viewer.js` → Delete (or just upload to replace)
3. Click "Upload Files"
4. Select `~/glmp/glmp-v2/viewer/viewer.js`
5. Done!

---

## 🧪 Test the Fixed Viewer

### **Step 1: Open the Viewer**
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html

### **Step 2: Open Browser DevTools**
- Press `F12` or right-click → Inspect
- Go to **Console** tab

### **Step 3: Check Console Output**

You should see:
```
🔄 Loading GLMP processes from: https://storage.googleapis.com/.../metadata.json
📥 Response: 200 OK
✅ Loaded successfully: 65 processes
```

*Note: It should show 65 processes now (we added 5 more today!)*

### **Step 4: Visual Check**

✅ **Expected Results:**
- Process list displays (not stuck on "Loading...")
- 65 processes shown
- Grouped by organism:
  - E. coli (37 processes)
  - S. cerevisiae (21 processes)  
  - B. subtilis (2 processes)
- "Back to Home" button is **hidden** on main page

### **Step 5: Click a Process**

Click "Lac Operon Regulation" (or any process)

✅ **Expected:**
- Flowchart loads and displays
- "Back to Home" button **appears**
- Mermaid diagram renders
- Citations display

### **Step 6: Click Back**

Click "Back to Home"

✅ **Expected:**
- Returns to process list
- "Back to Home" button **disappears** again

---

## 🔍 Troubleshooting

### **If process list doesn't load:**

1. **Hard refresh** the page: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. **Check console** for errors
3. **Verify deployment**: 
   ```bash
   gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/viewer.js | grep "storage.googleapis.com"
   ```
   Should show the absolute URLs, not `../processes/`

### **If you see CORS errors:**

Make sure files are publicly readable:
```bash
gsutil acl ch -u AllUsers:R \
  gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/*
```

### **If old version loads:**

Clear browser cache or use incognito mode

---

## 📊 Current Status

**Processes Available:**
- **Total:** 65 processes (up from 58!)
- **E. coli:** 37 processes
- **Yeast:** 21 processes  
- **Bacillus:** 2 processes

**New Processes Added Today:**
1. DNA Replication Elongation
2. DNA Replication Termination
3. Base Excision Repair
4. Nucleotide Excision Repair
5. Mismatch Repair
6. Translation Initiation
7. (Translation Elongation - in progress)

**Publication Progress:** 65/100 (65% complete)

---

## ✅ Deployment Checklist

- [ ] Pull latest changes from GitHub
- [ ] Upload fixed viewer.js to GCS
- [ ] Open viewer URL in browser
- [ ] Check browser console for success messages
- [ ] Verify 65 processes display
- [ ] Test clicking a process
- [ ] Test back button
- [ ] Clear any old browser cache
- [ ] Verify on different browser/incognito

---

## 🎉 Success Criteria

After deployment, you should have:

✅ **Viewer loads** all 65 processes  
✅ **Database table shows** all processes  
✅ **Both interfaces work** perfectly  
✅ **No more "Loading..." stuck screen**  
✅ **Proper navigation** with back button  
✅ **Console shows** helpful debug messages  

---

**Ready to deploy! Just run the commands above.** 🚀

---

*Fixed: October 16, 2025*  
*Deployed by: [Your deployment timestamp here]*
