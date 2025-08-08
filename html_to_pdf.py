#!/usr/bin/env python3
"""
Convert HTML proposal to PDF using weasyprint.
"""

import os
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_html_to_pdf():
    # Read the HTML file
    with open('ProcessDSL_FlowCell10_Proposal.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create font configuration
    font_config = FontConfiguration()
    
    # Convert HTML to PDF
    html_doc = HTML(string=html_content)
    pdf = html_doc.write_pdf(font_config=font_config)
    
    # Save the PDF
    with open('ProcessDSL_FlowCell10_Proposal.pdf', 'wb') as f:
        f.write(pdf)
    
    print("PDF created: ProcessDSL_FlowCell10_Proposal.pdf")

if __name__ == "__main__":
    convert_html_to_pdf() 