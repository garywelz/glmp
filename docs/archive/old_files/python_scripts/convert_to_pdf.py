#!/usr/bin/env python3
"""
Convert HTML article to PDF for Nature submission
"""

import subprocess
import sys
import os

def convert_html_to_pdf():
    """Convert programming_framework_article.html to PDF"""
    
    html_file = "programming_framework_article.html"
    pdf_file = "programming_framework_article.pdf"
    
    if not os.path.exists(html_file):
        print(f"❌ HTML file '{html_file}' not found!")
        return False
    
    print(f"🔄 Converting {html_file} to {pdf_file}...")
    
    # Try multiple conversion methods
    methods = [
        # Method 1: wkhtmltopdf
        lambda: subprocess.run([
            "wkhtmltopdf", "--page-size", "A4", "--margin-top", "1in",
            "--margin-bottom", "1in", "--margin-left", "1in", "--margin-right", "1in",
            html_file, pdf_file
        ], capture_output=True, text=True),
        
        # Method 2: weasyprint
        lambda: subprocess.run([
            sys.executable, "-m", "weasyprint", html_file, pdf_file
        ], capture_output=True, text=True),
        
        # Method 3: pandoc
        lambda: subprocess.run([
            "pandoc", html_file, "-o", pdf_file, "--pdf-engine=wkhtmltopdf"
        ], capture_output=True, text=True),
        
        # Method 4: Chrome headless
        lambda: subprocess.run([
            "google-chrome", "--headless", "--disable-gpu", "--print-to-pdf=" + pdf_file,
            "--print-to-pdf-no-header", html_file
        ], capture_output=True, text=True),
        
        # Method 5: Chromium headless
        lambda: subprocess.run([
            "chromium-browser", "--headless", "--disable-gpu", "--print-to-pdf=" + pdf_file,
            "--print-to-pdf-no-header", html_file
        ], capture_output=True, text=True)
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"  Trying method {i}...")
            result = method()
            
            if result.returncode == 0 and os.path.exists(pdf_file):
                print(f"✅ Successfully converted to {pdf_file}")
                print(f"📁 File size: {os.path.getsize(pdf_file)} bytes")
                return True
            else:
                print(f"  Method {i} failed: {result.stderr}")
                
        except FileNotFoundError:
            print(f"  Method {i} not available")
            continue
        except Exception as e:
            print(f"  Method {i} error: {e}")
            continue
    
    # Fallback: Create instructions for manual conversion
    print("❌ No conversion tools available.")
    create_manual_instructions()
    return False

def create_manual_instructions():
    """Create instructions for manual PDF conversion"""
    
    instructions = '''# Manual PDF Conversion Instructions

## Option 1: Browser Print to PDF
1. Open programming_framework_article.html in your browser
2. Press Ctrl+P (or Cmd+P on Mac)
3. Select "Save as PDF"
4. Set margins to 1 inch
5. Save as programming_framework_article.pdf

## Option 2: Online Converter
1. Go to https://www.ilovepdf.com/html_to_pdf
2. Upload programming_framework_article.html
3. Download the PDF

## Option 3: Install Conversion Tool
```bash
# Install wkhtmltopdf
sudo apt-get install wkhtmltopdf

# Then run:
wkhtmltopdf --page-size A4 programming_framework_article.html programming_framework_article.pdf
```

## Option 4: Google Docs
1. Open Google Docs
2. File > Import > Upload programming_framework_article.html
3. File > Download > PDF Document
'''
    
    with open('pdf_conversion_instructions.txt', 'w') as f:
        f.write(instructions)
    
    print("✅ Created pdf_conversion_instructions.txt")

if __name__ == "__main__":
    print("🔄 Converting HTML article to PDF for Nature submission...")
    success = convert_html_to_pdf()
    
    if success:
        print("\n🎉 Success! Your PDF is ready for Nature submission.")
        print("📝 Next steps:")
        print("1. Review the PDF for formatting")
        print("2. Create high-resolution figures")
        print("3. Prepare supplementary materials")
    else:
        print("\n💡 Use the manual instructions in pdf_conversion_instructions.txt")

