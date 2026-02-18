# Deployment Checklist

## What We've Done

### 1. Modularized Viewer Code ✅
- Created 8 modules in `glmp-v2/viewer/modules/`
- Refactored `viewer.js` from 1,365 lines to ~250 lines
- Removed 250 lines of unused chat modal code
- All modules are ready and tested locally

### 2. Updated Main index.html ✅
- Confirmed it has header with title and About button
- Frame loads `glmp-database-table.html` correctly
- This matches what's on Hugging Face

### 3. Cleaned Up Viewer index.html ✅
- Removed header (since it's in a frame)
- Simplified to just show the table
- Ready for future use

## What Needs to Be Deployed

### Option 1: Deploy Modularized Viewer (Recommended for Future)
**Files to deploy:**
- `glmp-v2/viewer/viewer.js` (refactored)
- `glmp-v2/viewer/modules/*.js` (all 8 modules)
- `glmp-v2/viewer/index.html` (simplified)
- `glmp-v2/viewer/metadata.json` (local copy for testing)

**Command:**
```bash
cd /home/gdubs/glmp
gsutil -m cp -r glmp-v2/viewer/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
```

**Note:** This is ready but not urgent since the main page uses the database table, not the viewer.

### Option 2: Just Deploy Main index.html (If Changed)
**Files to deploy:**
- `index.html` (main page with frame)

**Command:**
```bash
cd /home/gdubs/glmp
gsutil cp index.html gs://regal-scholar-453620-r7-podcast-storage/
```

**Note:** Only needed if you made changes to index.html that aren't already deployed.

## Current Status

✅ **Main page (index.html)**: Working correctly, matches Hugging Face
✅ **Database table**: Already deployed and working
✅ **Modularized viewer**: Ready but not deployed yet

## Recommendation

Since everything is working correctly and matches Hugging Face:
1. **No urgent deployment needed** - everything is already working
2. **Optional**: Deploy modularized viewer when ready to use it
3. **Future**: The modularized viewer can be used when you want to switch from database table to the simpler viewer

## Next Steps (Optional)

If you want to deploy the modularized viewer for future use:
```bash
# Deploy viewer and modules
gsutil -m cp -r glmp-v2/viewer/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/

# Verify deployment
gsutil ls gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/modules/
```



