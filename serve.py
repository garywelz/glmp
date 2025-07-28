#!/usr/bin/env python3
"""
Simple HTTP server for the Genome Logic Modeling Project website
Usage: python serve.py [port]
"""

import http.server
import socketserver
import sys
import os
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🧬 Genome Logic Modeling Project server starting...")
        print(f"📡 Serving at http://localhost:{PORT}")
        print(f"📄 Full paper available at: http://localhost:{PORT}/docs/paper/genome-logic-modeling.md")
        print(f"🔬 Repository structure at: http://localhost:{PORT}/")
        print(f"⏹️  Press Ctrl+C to stop the server")
        
        try:
            # Try to open the browser automatically
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
            
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped.")