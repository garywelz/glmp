#!/usr/bin/env python3
"""
Convert SVG to PNG for Medium upload
"""

import subprocess
import os
import sys

def convert_svg_to_png():
    """Convert SVG to PNG using cairosvg or rsvg-convert"""
    
    svg_file = "beta_galactosidase_flowchart.svg"
    png_file = "beta_galactosidase_flowchart.png"
    
    if not os.path.exists(svg_file):
        print(f"❌ SVG file '{svg_file}' not found!")
        return False
    
    print(f"🔄 Converting {svg_file} to {png_file}...")
    
    # Try multiple conversion methods
    methods = [
        # Method 1: cairosvg (Python library)
        lambda: subprocess.run([
            sys.executable, "-m", "cairosvg", 
            svg_file, "-o", png_file, "--width", "1200"
        ], capture_output=True, text=True),
        
        # Method 2: rsvg-convert (librsvg)
        lambda: subprocess.run([
            "rsvg-convert", "-w", "1200", 
            svg_file, "-o", png_file
        ], capture_output=True, text=True),
        
        # Method 3: ImageMagick
        lambda: subprocess.run([
            "convert", "-density", "300", 
            svg_file, "-resize", "1200x", png_file
        ], capture_output=True, text=True),
        
        # Method 4: Inkscape (if available)
        lambda: subprocess.run([
            "inkscape", "--export-type=png", 
            f"--export-filename={png_file}",
            "--export-width=1200", svg_file
        ], capture_output=True, text=True)
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"  Trying method {i}...")
            result = method()
            
            if result.returncode == 0 and os.path.exists(png_file):
                print(f"✅ Successfully converted to {png_file}")
                print(f"📁 File size: {os.path.getsize(png_file)} bytes")
                return True
            else:
                print(f"  Method {i} failed: {result.stderr}")
                
        except FileNotFoundError:
            print(f"  Method {i} not available")
            continue
        except Exception as e:
            print(f"  Method {i} error: {e}")
            continue
    
    # Fallback: Create a simple HTML viewer
    print("❌ No conversion tools available. Creating HTML viewer...")
    create_html_viewer()
    return False

def create_html_viewer():
    """Create an HTML file to view the SVG and take a screenshot"""
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>β-Galactosidase Flowchart for Medium</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: white;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        .svg-container {
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
        }
        .instructions {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>β-Galactosidase Flowchart for Medium</h1>
        
        <div class="instructions">
            <h3>📋 Instructions for Medium:</h3>
            <ol style="text-align: left;">
                <li><strong>Take a screenshot</strong> of the flowchart below</li>
                <li><strong>Save as PNG</strong> file</li>
                <li><strong>Upload to Medium</strong> as an image</li>
                <li><strong>Add caption</strong>: "The 2025 version: 20 minutes using Mermaid, Canvas, and LLMs"</li>
            </ol>
        </div>
        
        <div class="svg-container">
            <img src="beta_galactosidase_flowchart.svg" 
                 alt="β-Galactosidase Flowchart" 
                 style="max-width: 100%; height: auto;"
                 onerror="this.style.display='none'; document.getElementById('error').style.display='block';">
            <div id="error" style="display: none; color: red; padding: 20px;">
                <p>SVG file not found. Please ensure 'beta_galactosidase_flowchart.svg' is in the same directory.</p>
            </div>
        </div>
        
        <div style="margin-top: 20px; color: #666;">
            <p><strong>Tip:</strong> Use browser zoom (Ctrl/Cmd +) to make the flowchart larger before taking a screenshot.</p>
        </div>
    </div>
</body>
</html>'''
    
    with open('view_svg_for_medium.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created view_svg_for_medium.html")
    print("🌐 Opening in browser for screenshot...")
    
    try:
        import webbrowser
        webbrowser.open('file://' + os.path.abspath('view_svg_for_medium.html'))
    except:
        print("📁 Open 'view_svg_for_medium.html' in your browser manually")

def install_conversion_tools():
    """Try to install conversion tools"""
    print("🔧 Attempting to install conversion tools...")
    
    try:
        # Try to install cairosvg
        subprocess.run([sys.executable, "-m", "pip", "install", "cairosvg"], 
                      capture_output=True, check=True)
        print("✅ Installed cairosvg")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install cairosvg")
        return False

if __name__ == "__main__":
    print("🔄 Converting SVG to PNG for Medium...")
    
    # Try conversion first
    success = convert_svg_to_png()
    
    if not success:
        print("\n💡 Alternative solutions:")
        print("1. Install conversion tools: pip install cairosvg")
        print("2. Use online converter: https://convertio.co/svg-png/")
        print("3. Use the HTML viewer I created")
        print("4. Take a screenshot of the SVG in a browser")
        
        # Try to install tools
        if install_conversion_tools():
            print("\n🔄 Retrying conversion...")
            convert_svg_to_png()

