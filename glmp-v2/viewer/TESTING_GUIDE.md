# Testing Guide for Modularized Viewer

## Quick Start - Local Testing

### Option 1: Python HTTP Server (Recommended)

If you have Python installed:

```bash
cd /home/gdubs/glmp/glmp-v2/viewer
python3 -m http.server 8000
```

Then open in browser:
```
http://localhost:8000
```

### Option 2: Node.js HTTP Server

If you have Node.js installed:

```bash
cd /home/gdubs/glmp/glmp-v2/viewer
npx http-server -p 8000
```

Then open in browser:
```
http://localhost:8000
```

### Option 3: PHP Built-in Server

If you have PHP installed:

```bash
cd /home/gdubs/glmp/glmp-v2/viewer
php -S localhost:8000
```

Then open in browser:
```
http://localhost:8000
```

## Testing Checklist

### 1. Initial Load
- [ ] Page loads without errors
- [ ] No console errors in browser DevTools
- [ ] Process list appears (or loading spinner)
- [ ] Navigation works

### 2. Process List
- [ ] Process list displays correctly
- [ ] Processes are sorted alphabetically
- [ ] Clicking a process loads it
- [ ] Table formatting looks correct

### 3. Process View
- [ ] Process details load correctly
- [ ] Title, organism, category display
- [ ] Mermaid diagram renders
- [ ] Color legend displays (if available)
- [ ] Citations display (if available)
- [ ] Metadata displays

### 4. Mermaid Diagram
- [ ] Diagram renders without errors
- [ ] Nodes are clickable
- [ ] Clicking nodes populates feedback form
- [ ] Detail level selector works (if multiple levels)
- [ ] Diagram updates when detail level changes

### 5. Feedback System
- [ ] Feedback panel initializes
- [ ] Process ID and name are visible
- [ ] Form fields work
- [ ] Node selection from diagram works
- [ ] Form submission works
- [ ] Success message appears
- [ ] Form resets after submission

### 6. Comments
- [ ] Comments section displays
- [ ] Existing comments load (if any)
- [ ] New comments appear after submission
- [ ] Comments format correctly

### 7. Navigation
- [ ] Back button works
- [ ] URL updates when loading process
- [ ] Browser back/forward buttons work
- [ ] Direct URL to process works

## Browser DevTools Checks

### Console Tab
Check for:
- ✅ No red errors
- ✅ Module imports successful
- ✅ Functions called correctly
- ⚠️ Any warnings (usually OK)

### Network Tab
Check for:
- ✅ `viewer.js` loads (200 status)
- ✅ All module files load (200 status)
- ✅ `metadata.json` loads
- ✅ Process JSON files load
- ⚠️ No 404 errors for modules

### Sources Tab
Verify:
- ✅ All modules appear in file tree
- ✅ Breakpoints can be set
- ✅ Code is readable

## Common Issues & Fixes

### Issue: "Failed to load module"
**Cause**: CORS or path issues
**Fix**: Make sure you're using HTTP server, not file://

### Issue: "Cannot find module"
**Cause**: Incorrect import path
**Fix**: Check import paths in viewer.js are relative (./modules/...)

### Issue: "Mermaid not defined"
**Cause**: Mermaid library not loaded
**Fix**: Check index.html has Mermaid script tag before viewer.js

### Issue: "Process not loading"
**Cause**: Network or path issues
**Fix**: Check browser console for fetch errors

## Testing on GCS

After local testing works:

1. **Deploy to GCS**:
```bash
cd /home/gdubs/glmp
gsutil -m cp -r glmp-v2/viewer/* gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/
```

2. **Test on GCS**:
   - Open: `https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html`
   - Or use your main viewer URL

3. **Verify**:
   - All modules load from GCS
   - CORS headers are correct
   - All features work

## Debug Mode

To enable verbose logging, check browser console for:
- 🚀 Initialization messages
- 📄 Process loading messages
- 🎨 Rendering messages
- ✅ Success messages
- ❌ Error messages

## Quick Test Script

Create a simple test HTML file to verify modules load:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Module Test</title>
</head>
<body>
    <h1>Module Test</h1>
    <div id="test-output"></div>
    <script type="module">
        import { CONFIG } from './modules/config.js';
        document.getElementById('test-output').textContent = 
            'Config loaded: ' + CONFIG.metadataPath;
        console.log('✅ Modules working!');
    </script>
</body>
</html>
```

If this works, modules are loading correctly!



