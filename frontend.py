#!/usr/bin/env python3
"""
IAM Chatbot Frontend - Main Entry
Start HTTP server to serve frontend files
"""

import os
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

def start_frontend():
    # Ensure we're in the project directory
    os.chdir(Path(__file__).parent)
    
    print("")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  🌐 IAM Chatbot Frontend Started                        ║")
    print(f"║  📍 Access URL: http://localhost:{PORT:<3}                           ║")
    print("║  ⚠️  Press Ctrl+C to stop the server                     ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("")
    
    # Try to open the browser
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        pass
    
    # Start the server
    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Frontend service stopped")

if __name__ == "__main__":
    start_frontend()
