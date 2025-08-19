#!/usr/bin/env python3
"""
Fix Duplicate Color Keys Script
Removes duplicate color keys that were accidentally added during the update process.
"""

import os
import re
import glob
from pathlib import Path

def fix_duplicate_color_keys(file_path):
    """Remove duplicate color keys from a single HTML file."""
    print(f"Fixing duplicates in: {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find duplicate color keys
    # Look for two consecutive color key divs with the same content
    color_key_pattern = r'<div style="display: grid; grid-template-columns: repeat\(auto-fit,minmax\(140px,1fr\)\); gap: \.5rem 1rem; margin: 1rem 0 0; font-size: 10pt; color: #333;">.*?</div>'
    
    # Find all color keys
    color_keys = re.findall(color_key_pattern, content, re.DOTALL)
    
    if len(color_keys) > 1:
        # Keep only the first color key, remove duplicates
        first_color_key = color_keys[0]
        
        # Replace all color keys with just the first one
        content = re.sub(color_key_pattern, first_color_key, content, flags=re.DOTALL)
        
        # Write updated content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {file_path} - Removed {len(color_keys)-1} duplicate color keys")
    else:
        print(f"✅ No duplicates found in: {file_path}")

def main():
    """Main function to fix duplicate color keys in all HTML files."""
    print("🔧 Fixing Duplicate Color Keys")
    print("=" * 40)
    
    # Find all HTML files
    html_files = glob.glob("*.html") + glob.glob("*/*.html") + glob.glob("*/*/*.html")
    
    # Filter out any files we don't want to update
    exclude_patterns = ['index.html', 'README.html', 'template.html']
    html_files = [f for f in html_files if not any(pattern in f for pattern in exclude_patterns)]
    
    print(f"Found {len(html_files)} HTML files to check")
    
    # Process each file
    for file_path in html_files:
        try:
            fix_duplicate_color_keys(file_path)
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n🎉 Duplicate color key fix complete!")

if __name__ == "__main__":
    main()
