#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IAM Chatbot backend entry point
Start Flask API service
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (force override)
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    print("\u274c Error: .env file not found")
    print("Please run: python configure.py first")
    sys.exit(1)

# Validate required environment variables
required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ Error: Missing environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# Import application
from app import app

if __name__ == "__main__":
    print("🚀 Starting IAM Chatbot backend service")
    print("📍 Listening on: http://127.0.0.1:5000")
    print("⚠️  Press Ctrl+C to stop server")
    print("")
    
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true", 
            host="127.0.0.1", 
            port=5000)
