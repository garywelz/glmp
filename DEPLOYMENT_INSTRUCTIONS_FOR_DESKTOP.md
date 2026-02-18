# 🚀 DEPLOYMENT INSTRUCTIONS - Desktop Agent

## 📋 **Quick Summary**

You need to deploy **3 user-reported processes** that have been fully fixed:
1. ✅ Amino Acid Biosynthesis (6 logic fixes)
2. ✅ Anaerobic Respiration (ALL bracket conflicts fixed)
3. ✅ Biofilm Formation (1 syntax fix)

---

## 🔧 **Run These Commands:**

```bash
cd ~/glmp
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
./DEPLOY_3_USER_REPORTED_ONLY.sh
```

**This will deploy only the 3 processes the user reported errors on.**

---

## 🎯 **Alternative: Deploy All 19 Processes**

If you want to deploy ALL 19 fixed processes (3 user-reported + 16 Phase 1):

```bash
cd ~/glmp
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
./DEPLOY_ALL_19_FIXED_PROCESSES.sh
```

**Either script will work!** The 3-process one is faster and focused.

---

## 🔍 **What Was Fixed:**

### **Anaerobic Respiration** (The Persistent Problem!)
**Root Cause:** Had `[4Fe-4S]` brackets in regular rectangle nodes
- `A8[... FNR has [4Fe-4S]2+ cluster]`
- `A10[O2 oxidizes [4Fe-4S]2+ cluster]`  
- `A14[FNR with intact [4Fe-4S]2+ cluster]`

**Fix:** Replaced ALL instances:
- `[4Fe-4S]` → `(4Fe-4S)`
- `[2Fe-2S]` → `(2Fe-2S)`

**Result:** Zero bracket conflicts, clean Mermaid rendering!

### **Biofilm Formation**
**Problem:** Wrong trapezoid syntax `Y[\Inactive State/]`  
**Fix:** Changed to `Y[/Inactive State/]`

### **Amino Acid Biosynthesis**
**Problem:** 6 logic gate errors (invalid AND gates, missing OR gates, trapezoid sequences)  
**Fix:** Added proper OR/AND gates, fixed terminal trapezoids

---

## 🚨 **CRITICAL: Cache Clearing After Deployment**

The user MUST aggressively clear cache:

1. **Close ALL browser windows**
2. **Clear ALL browser data:**
   - History
   - Cache  
   - Cookies
   - Everything
3. **Wait 5 minutes** for GCS/CDN propagation
4. **Open browser in INCOGNITO/PRIVATE mode**
5. Test the 3 processes

---

## 🔗 **Direct GCS Test Links** (Bypass ALL Cache)

After deployment, test with these direct links:

```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_amino_acid_biosynthesis

https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_anaerobic_respiration

https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_biofilm_formation
```

**These bypass HuggingFace and CDN cache completely!**

---

## ✅ **Expected Result**

After deployment + cache clearing:
- ✅ No "Syntax Error in text" messages
- ✅ All graphs render correctly
- ✅ All red trapezoids display properly
- ✅ Logic gates (OR/AND) show correctly

---

## 📝 **Note on Path Fixes**

Both deployment scripts now use **relative paths** (`./processes_with_not_gates/`) instead of absolute paths (`/workspace/...`), so they work correctly when run from `~/glmp`.

---

**Ready to deploy! Run `DEPLOY_3_USER_REPORTED_ONLY.sh` now!** 🚀
