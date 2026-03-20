#!/usr/bin/env python3
"""
IAM Chatbot Frontend - Main Entry
Start HTTP server to serve frontend files
"""

import os
import http.server
import socketserver
from pathlib import Path

# Use PORT from environment variable (Render sets this) or default to 8000
PORT = int(os.getenv("PORT", 8000))
HANDLER = http.server.SimpleHTTPRequestHandler

def start_frontend():
    # Ensure we're in the project directory
    os.chdir(Path(__file__).parent)
    
    print("")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  🌐 IAM Chatbot Frontend Started                        ║")
    print(f"║  📍 Listening on: 0.0.0.0:{PORT:<3}                           ║")
    print("║  ⚠️  Press Ctrl+C to stop the server                     ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("")
    
    # Start the server
    with socketserver.TCPServer(("0.0.0.0", PORT), HANDLER) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Frontend service stopped")

if __name__ == "__main__":
    start_frontend()
