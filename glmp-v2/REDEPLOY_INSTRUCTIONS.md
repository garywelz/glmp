# Redeploy Instructions - Maximum Complexity Upgrade

## 🎉 Upgrade Complete!

Your GLMP v2 viewer has been upgraded to **maximum complexity** with:
- ✅ **66-node lac operon** (from 10 nodes)
- ✅ **5-color Programming Framework scheme**
- ✅ **Color key legend** (displays inline)
- ✅ **Scientific accuracy statement**
- ✅ **Unique node identifiers** (A-III)

---

## 🚀 Redeploy to GCS (3 Commands)

Run these on your local machine where you deployed earlier:

```bash
# 1. Pull latest changes
cd ~/glmp-clean
git pull origin main

# 2. Navigate to deployment directory
cd glmp-v2

# 3. Redeploy
./DEPLOY_TO_GCS.sh
```

**Time: ~2 minutes**

---

## ✅ Verify Upgrade

After deployment, open this URL:

```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_lac_operon
```

### You Should See:

1. **Color Key Legend** - Beautiful grid showing all 5 color categories:
   - 🔴 Red - Triggers & Inputs
   - 🟡 Yellow - Structures & Objects
   - 🟢 Green - Processing & Operations
   - 🔵 Blue - Intermediates & States
   - 🟣 Violet - Products & Outputs

2. **Scientific Accuracy Statement** - Blue box validating data sources

3. **66-Node Flowchart** - Massive detailed diagram with:
   - Environmental sensing
   - Transport mechanisms
   - Regulatory logic gates
   - Transcription control
   - Protein synthesis
   - Metabolic pathways
   - Feedback regulation
   - Dynamic equilibrium

4. **All Original Citations** - 4 sources with PubMed IDs preserved

---

## 🎨 What Changed

### Before:
```
Simple flowchart:
  • 10 nodes
  • Generic colors
  • No legend
  • Basic description
```

### After:
```
Maximum complexity:
  • 66 unique nodes (A-III)
  • 5-color standard scheme
  • Inline color legend
  • Scientific validation
  • Full molecular detail
```

---

## 📊 Technical Details

### Upgraded Files:
1. `processes/ecoli/ecoli_lac_operon.json` - 66 nodes with color scheme
2. `viewer/index.html` - Added legend and accuracy sections
3. `viewer/viewer.js` - New rendering functions
4. `viewer/styles.css` - Styled color legend
5. `data/metadata.json` - Updated complexity metrics

### Color Hex Codes:
- Red: `#ff6b6b`
- Yellow: `#ffd43b`
- Green: `#51cf66`
- Blue: `#74c0fc`
- Violet: `#b197fc`

---

## 🔧 If Something Goes Wrong

### Issue: "Already up to date" when pulling
**Solution:**
```bash
cd ~/glmp-clean
git fetch origin
git reset --hard origin/main
cd glmp-v2
./DEPLOY_TO_GCS.sh
```

### Issue: Flowchart doesn't render
**Solution:**
1. Clear browser cache (Ctrl+Shift+R)
2. Wait 1-2 minutes for GCS cache
3. Try incognito mode

### Issue: Color legend doesn't show
**Solution:**
- Make sure you pulled the latest version
- Check browser console for errors
- Verify the JSON file deployed correctly

---

## 📋 Next Steps

After verifying the lac operon works:

### Option A: Deploy As-Is
- You now have 1 maximum-complexity process
- Other 3 processes remain at basic level
- Can upgrade others later

### Option B: Upgrade All 4 Processes
- Extract detailed versions from HuggingFace
- Convert DNA Replication, Transcription, Cell Cycle
- Deploy complete collection

**Recommendation: Test the lac operon first, then decide!**

---

## 🎯 Success Criteria

✅ Color legend displays with 5 categories  
✅ Scientific accuracy box shows (blue background)  
✅ 66-node flowchart renders without errors  
✅ All colors follow the 5-color scheme  
✅ Citations preserved with PubMed links  
✅ No "Syntax error" messages  

---

## 💬 Questions?

If you see any issues or want to upgrade the other 3 processes, just let me know!

**Ready to redeploy? Run the 3 commands above!** 🚀
