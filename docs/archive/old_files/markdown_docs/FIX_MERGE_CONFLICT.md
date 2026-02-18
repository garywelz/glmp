# 🚨 Fix Git Merge Conflict - Desktop Agent Instructions

**Issue:** Merge conflict when pulling from GitHub  
**Solution:** Abort merge, stash local changes, pull, then redeploy

---

## 🔧 QUICK FIX (Copy/Paste These Commands)

```bash
# 1. Abort the failed merge
git merge --abort

# 2. Stash any local changes
git stash

# 3. Pull from GitHub (clean)
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90

# 4. Check that deployment script exists
ls -lh DEPLOY_ALL_VIEWER_FIXES.sh

# 5. Run deployment
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### Step 1: Abort the Merge
```bash
cd ~/glmp
git merge --abort
```
**This cancels the failed merge and returns to a clean state.**

### Step 2: Stash Local Changes (if any)
```bash
git stash
```
**This saves any uncommitted local changes temporarily.**

### Step 3: Pull Latest Code
```bash
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
```
**Expected output:**
```
From https://github.com/garywelz/glmp
 * branch            cursor/continue-frozen-deploy-glmp-conversation-0c90 -> FETCH_HEAD
Updating ...
Fast-forward
 DEPLOY_ALL_VIEWER_FIXES.sh | 150 ++++++++++++++++++++++++++
 ...
```

### Step 4: Verify Script Exists
```bash
ls -lh DEPLOY_ALL_VIEWER_FIXES.sh
```
**Expected:** Should show the file with executable permissions (-rwxr-xr-x)

**If file not found:**
```bash
# Make sure you're in the right directory
pwd
# Should show: /home/gdubs/glmp

# List all deployment scripts
ls -lh *.sh
```

### Step 5: Run Deployment
```bash
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

---

## ⚠️ IF STEP 3 STILL SHOWS MERGE CONFLICT

### Option A: Reset to Remote (Safe - Recommended)
```bash
# Save current state just in case
git stash

# Reset to match remote exactly
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git reset --hard origin/cursor/continue-frozen-deploy-glmp-conversation-0c90

# Verify clean state
git status
```
**Expected output:** "Your branch is up to date with 'origin/cursor/continue-frozen-deploy-glmp-conversation-0c90'."

### Option B: Manual Merge (If you have local changes to keep)
```bash
# See what files are conflicting
git status

# For each conflicting file, choose remote version:
git checkout --theirs <filename>

# Or choose your local version:
git checkout --ours <filename>

# After resolving all conflicts:
git add .
git commit -m "Resolved merge conflicts"
```

---

## 🎯 ALTERNATIVE: Direct Deployment (Bypass Git)

**If git issues persist, you can deploy directly:**

### Download Files Directly from GitHub

```bash
cd ~/glmp

# Download the deployment script
curl -o DEPLOY_ALL_VIEWER_FIXES.sh \
  'https://raw.githubusercontent.com/garywelz/glmp/cursor/continue-frozen-deploy-glmp-conversation-0c90/DEPLOY_ALL_VIEWER_FIXES.sh'

# Make it executable
chmod +x DEPLOY_ALL_VIEWER_FIXES.sh

# Download the viewer files
curl -o glmp-v2/viewer/index.html \
  'https://raw.githubusercontent.com/garywelz/glmp/cursor/continue-frozen-deploy-glmp-conversation-0c90/glmp-v2/viewer/index.html'

curl -o glmp-v2/viewer/viewer.js \
  'https://raw.githubusercontent.com/garywelz/glmp/cursor/continue-frozen-deploy-glmp-conversation-0c90/glmp-v2/viewer/viewer.js'

curl -o glmp-v2/viewer/styles.css \
  'https://raw.githubusercontent.com/garywelz/glmp/cursor/continue-frozen-deploy-glmp-conversation-0c90/glmp-v2/viewer/styles.css'

# Now run deployment
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

---

## 🔍 TROUBLESHOOTING

### Issue: "fatal: Not possible to fast-forward, aborting."
**Solution:** Use Option A (reset to remote)

### Issue: "error: Your local changes to the following files would be overwritten"
**Solution:** 
```bash
git stash
git pull origin cursor/continue-frozen-deploy-glmp-conversation-0c90
```

### Issue: "DEPLOY_ALL_VIEWER_FIXES.sh: No such file or directory"
**Cause:** Pull didn't complete successfully  
**Solution:** Use Alternative Direct Deployment above

### Issue: "permission denied"
**Solution:**
```bash
chmod +x DEPLOY_ALL_VIEWER_FIXES.sh
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

---

## ✅ VERIFICATION

After successful pull, verify these files exist:

```bash
cd ~/glmp
ls -lh DEPLOY_ALL_VIEWER_FIXES.sh
ls -lh glmp-v2/viewer/index.html
ls -lh glmp-v2/viewer/viewer.js
ls -lh glmp-v2/viewer/styles.css
```

**All should exist.**

Then run deployment:
```bash
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

---

## 📞 WHAT TO REPORT BACK

After trying the fix, let me know:

1. **Which method worked:**
   - [ ] Standard pull (after git merge --abort)
   - [ ] Reset to remote (Option A)
   - [ ] Direct download (Alternative)

2. **Current status:**
   - [ ] Deployment script found
   - [ ] Deployment script ran successfully
   - [ ] Files uploaded to GCS
   - [ ] Viewer tested in incognito mode

3. **Any errors encountered:**
   - Copy/paste any error messages

---

## 🚀 QUICK SUMMARY

**Fastest path to success:**

```bash
cd ~/glmp
git merge --abort
git stash
git fetch origin cursor/continue-frozen-deploy-glmp-conversation-0c90
git reset --hard origin/cursor/continue-frozen-deploy-glmp-conversation-0c90
bash DEPLOY_ALL_VIEWER_FIXES.sh
```

**That's it!** 5 commands, ~2 minutes.

---

**Desktop Agent: Try the Quick Summary commands first!** 🎯
