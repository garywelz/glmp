#!/usr/bin/env python3
"""
Convert GLMP paper HTML to PDF using Chromium headless mode
"""

import subprocess
import os
import sys

def convert_html_to_pdf():
    """Convert glmp_paper_v2.html to PDF using Chromium"""
    
    # Get absolute path to the HTML file
    html_file = os.path.abspath("glmp_paper_v2.html")
    pdf_file = "glmp_paper_v2.pdf"
    
    print(f"Converting {html_file} to {pdf_file}...")
    
    # Chromium command for PDF conversion
    cmd = [
        "chromium-browser",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--print-to-pdf=" + pdf_file,
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--margin-top=0.5in",
        "--margin-bottom=0.5in", 
        "--margin-left=0.5in",
        "--margin-right=0.5in",
        "--page-size=Letter",
        "--disable-extensions",
        "--disable-plugins",
        "file://" + html_file
    ]
    
    try:
        # Run the conversion
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ PDF created successfully: {pdf_file}")
            print(f"File size: {os.path.getsize(pdf_file)} bytes")
            return True
        else:
            print(f"❌ Error creating PDF:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Conversion timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = convert_html_to_pdf()
    if success:
        print("\n🎉 PDF ready for bioRxiv submission!")
        print("File: glmp_paper_v2.pdf")
    else:
        print("\n❌ PDF conversion failed")
        sys.exit(1)
