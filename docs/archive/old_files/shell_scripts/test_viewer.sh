#!/bin/bash
# Quick test script for GLMP Viewer

echo "🧪 GLMP Viewer Test Script"
echo "=========================="
echo ""

# Check if we're in the right directory
if [ ! -d "glmp-v2/viewer" ]; then
    echo "❌ Error: glmp-v2/viewer directory not found"
    echo "   Please run this script from the glmp root directory"
    exit 1
fi

cd glmp-v2/viewer

# Check for Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    echo ""
    echo "Starting HTTP server on port 8000..."
    echo "Open these URLs in your browser:"
    echo "  - Module test: http://localhost:8000/test_modules.html"
    echo "  - Full viewer: http://localhost:8000/index.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "✅ Python found"
    echo ""
    echo "Starting HTTP server on port 8000..."
    echo "Open these URLs in your browser:"
    echo "  - Module test: http://localhost:8000/test_modules.html"
    echo "  - Full viewer: http://localhost:8000/index.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python -m SimpleHTTPServer 8000
else
    echo "❌ Python not found"
    echo ""
    echo "Please install Python 3, or use one of these alternatives:"
    echo "  - Node.js: npx http-server -p 8000"
    echo "  - PHP: php -S localhost:8000"
    exit 1
fi
