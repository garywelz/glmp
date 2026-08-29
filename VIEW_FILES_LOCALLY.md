# How to View GLMP Files Locally

## Problem
The links in the workspace aren't clickable, making it difficult to preview HTML files.

## Solutions

### Option 1: Start a Local Web Server (Recommended)

The easiest way to view all files with proper formatting:

```bash
cd /workspace
python3 -m http.server 8000
```

Then open in your browser:
- **Main page**: http://localhost:8000/index.html
- **Biology processes**: http://localhost:8000/biological_processes/index.html
- **E. coli files**: http://localhost:8000/biological_processes/ecoli/
- **Yeast files**: http://localhost:8000/biological_processes/yeast/

### Option 2: Open Files Directly in Browser

Navigate to the file in your file browser and open with your default browser:

```bash
# On Linux
xdg-open /workspace/index.html

# On Mac
open /workspace/index.html

# On Windows
start /workspace/index.html
```

### Option 3: Use VS Code Preview (if available)

If you're in VS Code:
1. Right-click on any HTML file
2. Select "Open with Live Server" or "Preview"

### Option 4: Copy Path and Open Manually

Copy the full file path and paste into browser address bar:

**Example paths to try:**
```
file:///workspace/index.html
file:///workspace/GLMP_Foundation.html
file:///workspace/biological_processes/index.html
file:///workspace/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html
file:///workspace/biological_processes/yeast/yeast_batch01_dna_replication_repair.html
```

## Recommended Viewing Order

1. **Start with the main index**:
   - `/workspace/index.html` - Project overview

2. **View the foundation page**:
   - `/workspace/GLMP_Foundation.html` - Historical context

3. **Browse biological processes**:
   - `/workspace/biological_processes/index.html` - Process catalog

4. **Explore E. coli processes** (new from standardization):
   - `/workspace/biological_processes/ecoli/ecoli_batch01_dna_replication_repair.html`
   - `/workspace/biological_processes/ecoli/ecoli_batch02_cell_division_segregation.html`
   - etc. (15 total)

5. **Explore yeast processes** (new from standardization):
   - `/workspace/biological_processes/yeast/yeast_batch01_dna_replication_repair.html`
   - `/workspace/biological_processes/yeast/yeast_batch02_cell_cycle_control.html`
   - etc. (23 total)

## Quick File Listing

### Top-Level HTML Files
```bash
ls -1 /workspace/*.html
```

### E. coli Files
```bash
ls -1 /workspace/biological_processes/ecoli/*.html
```

### Yeast Files
```bash
ls -1 /workspace/biological_processes/yeast/*.html
```

## Using the Python Server (Detailed)

The Python HTTP server is the best option because:
- ✅ Preserves all formatting and styles
- ✅ Allows clicking links between pages
- ✅ Shows images correctly
- ✅ No security restrictions (unlike file:// URLs)

**Start the server:**
```bash
cd /workspace
python3 -m http.server 8000
```

**Access files:**
- Main: http://localhost:8000/
- Any file: http://localhost:8000/path/to/file.html

**Stop the server:**
Press `Ctrl+C` in the terminal

## Alternative: Simple Python Script

Create a quick launcher:

```bash
cat > /workspace/view.sh << 'EOF'
#!/bin/bash
echo "Starting local web server..."
echo "Open your browser to: http://localhost:8000"
echo "Press Ctrl+C to stop"
cd /workspace
python3 -m http.server 8000
EOF

chmod +x /workspace/view.sh
./view.sh
```

## File Count Summary

After the standardization work, you have:
- **38** biological process HTML files (15 E. coli + 23 yeast)
- **1** biological processes index
- **5** Python scripts for generation
- **Multiple** template and support files

All files are in `/workspace/biological_processes/`

## Quick Preview Without Browser

To quickly view the content of an HTML file in the terminal:

```bash
# View as text (strips HTML tags)
python3 -c "from html.parser import HTMLParser; import sys; \
class TextExtractor(HTMLParser): \
    def handle_data(self, data): print(data.strip()) if data.strip() else None; \
parser = TextExtractor(); \
parser.feed(open('/workspace/index.html').read())"

# Or use a simple grep
grep -o "<title>.*</title>" /workspace/index.html
grep -o "<h1>.*</h1>" /workspace/index.html
```

But really, the Python web server (Option 1) is your best bet for proper viewing!
