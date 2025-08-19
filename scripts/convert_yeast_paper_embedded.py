#!/usr/bin/env python3
"""
Convert yeast process flowcharts HTML paper to PDF with embedded SVG images.
"""

import sys
import os
import base64
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def embed_svg_images(html_content):
    """Embed SVG images as base64 data URLs in the HTML content."""
    import re
    
    # Find all img tags with SVG files
    img_pattern = r'<img src="([^"]*\.svg)"([^>]*)>'
    
    def replace_img(match):
        img_src = match.group(1)
        img_attrs = match.group(2)
        
        # Convert relative path to absolute path
        if img_src.startswith('docs/'):
            img_path = img_src
        else:
            img_path = img_src
            
        try:
            # Read the SVG file
            with open(img_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            # Encode as base64
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            data_url = f"data:image/svg+xml;base64,{svg_base64}"
            
            return f'<img src="{data_url}"{img_attrs}>'
        except Exception as e:
            print(f"Warning: Could not embed {img_path}: {e}")
            return match.group(0)  # Keep original if embedding fails
    
    return re.sub(img_pattern, replace_img, html_content)

def convert_html_to_pdf(input_html, output_pdf):
    # Read the HTML file
    with open(input_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Embed SVG images
    html_content = embed_svg_images(html_content)
    
    # Create font configuration
    font_config = FontConfiguration()
    
    # Convert HTML to PDF
    html_doc = HTML(string=html_content)
    pdf = html_doc.write_pdf(font_config=font_config)
    
    # Save the PDF
    with open(output_pdf, 'wb') as f:
        f.write(pdf)
    
    print(f"PDF created with embedded images: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_yeast_paper_embedded.py input.html output.pdf")
        sys.exit(1)
    
    input_html = sys.argv[1]
    output_pdf = sys.argv[2]
    
    convert_html_to_pdf(input_html, output_pdf)

