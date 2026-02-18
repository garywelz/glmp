#!/usr/bin/env python3
"""
Upload SVG to Google Cloud Storage for Medium linking
"""

import os
import subprocess
from datetime import datetime

def upload_to_gcs():
    """Upload SVG to Google Cloud Storage"""
    
    svg_file = "beta_galactosidase_flowchart.svg"
    
    if not os.path.exists(svg_file):
        print(f"❌ SVG file '{svg_file}' not found!")
        return False
    
    # GCS bucket and path (using your existing bucket)
    bucket_name = "regal-scholar-453620-r7-podcast-storage"
    gcs_path = "glmp/docs/paper/figures/medium/beta_galactosidase_flowchart.svg"
    
    print(f"🔄 Uploading {svg_file} to GCS...")
    print(f"📁 Bucket: {bucket_name}")
    print(f"📍 Path: {gcs_path}")
    
    try:
        # Upload using gsutil
        cmd = [
            "gsutil", "cp", svg_file, 
            f"gs://{bucket_name}/{gcs_path}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Create public URL
            public_url = f"https://storage.googleapis.com/{bucket_name}/{gcs_path}"
            
            print("✅ Successfully uploaded to GCS!")
            print(f"🔗 Public URL: {public_url}")
            
            # Create HTML snippet for Medium
            html_snippet = f'''<div style="text-align: center; margin: 20px 0;">
    <img src="{public_url}" 
         alt="2025 β-Galactosidase Flowchart - Programming Framework Analysis" 
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <p style="font-style: italic; color: #666; margin-top: 10px;">
        The 2025 version: 20 minutes using Mermaid, Canvas, and LLMs
    </p>
</div>'''
            
            # Save HTML snippet to file
            with open("medium_image_snippet.html", "w") as f:
                f.write(html_snippet)
            
            print("\n📋 HTML snippet saved to 'medium_image_snippet.html'")
            print("📝 Copy this HTML and paste it into Medium's HTML editor mode")
            
            return True
            
        else:
            print(f"❌ Upload failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ gsutil not found. Please install Google Cloud SDK")
        print("💡 Alternative: Upload manually to GCS and use the public URL")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_alternative_upload_instructions():
    """Create instructions for manual upload"""
    
    instructions = f"""# Manual GCS Upload Instructions

## Option 1: Google Cloud Console
1. Go to https://console.cloud.google.com/storage/browser
2. Navigate to: regal-scholar-453620-r7-podcast-storage/glmp/docs/paper/figures/medium/
3. Upload: beta_galactosidase_flowchart.svg
4. Make file public (right-click → "Make public")
5. Copy the public URL

## Option 2: gsutil Command Line
```bash
gsutil cp beta_galactosidase_flowchart.svg gs://regal-scholar-453620-r7-podcast-storage/glmp/docs/paper/figures/medium/
gsutil acl ch -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/docs/paper/figures/medium/beta_galactosidase_flowchart.svg
```

## Option 3: Alternative Storage Services
- **GitHub**: Upload to your repository and use raw.githubusercontent.com URL
- **Hugging Face**: Upload to your HF space and use the direct file URL
- **Dropbox**: Upload and get a direct link
- **Google Drive**: Upload and get a shareable link

## For Medium:
Once you have the public URL, use this HTML in Medium's HTML editor:

```html
<div style="text-align: center; margin: 20px 0;">
    <img src="YOUR_PUBLIC_URL_HERE" 
         alt="2025 β-Galactosidase Flowchart - Programming Framework Analysis" 
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <p style="font-style: italic; color: #666; margin-top: 10px;">
        The 2025 version: 20 minutes using Mermaid, Canvas, and LLMs
    </p>
</div>
```
"""
    
    with open("gcs_upload_instructions.md", "w") as f:
        f.write(instructions)
    
    print("📋 Manual upload instructions saved to 'gcs_upload_instructions.md'")

if __name__ == "__main__":
    print("🚀 Uploading SVG to Google Cloud Storage for Medium...")
    
    success = upload_to_gcs()
    
    if not success:
        print("\n💡 Creating manual upload instructions...")
        create_alternative_upload_instructions()
        
        print("\n🎯 Quick Solutions:")
        print("1. Upload to your existing GCS bucket manually")
        print("2. Use GitHub raw file URL")
        print("3. Upload to Hugging Face and link directly")
        print("4. Use any cloud storage service with public URLs")

