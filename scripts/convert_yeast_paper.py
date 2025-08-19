#!/usr/bin/env python3
"""
Convert yeast process flowcharts HTML paper to PDF using weasyprint.
"""

import sys
import os
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_html_to_pdf(input_html, output_pdf):
    # Read the HTML file
    with open(input_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create font configuration
    font_config = FontConfiguration()
    
    # Convert HTML to PDF
    html_doc = HTML(string=html_content)
    pdf = html_doc.write_pdf(font_config=font_config)
    
    # Save the PDF
    with open(output_pdf, 'wb') as f:
        f.write(pdf)
    
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_yeast_paper.py input.html output.pdf")
        sys.exit(1)
    
    input_html = sys.argv[1]
    output_pdf = sys.argv[2]
    
    convert_html_to_pdf(input_html, output_pdf)

