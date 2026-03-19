#!/usr/bin/env python3

import os
from pathlib import Path

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "hackathon"

AWS_REGION = "us-east-1"
AWS_ACCESS_KEY_ID = "your_access_key_here"  # Replace with your AWS access key
AWS_SECRET_ACCESS_KEY = "your_secret_key_here"  # Replace with your AWS secret key
AWS_BEARER_TOKEN_BEDROCK = "your_bearer_token_here"  # Replace with your Bedrock token
OPENAI_API_KEY = AWS_BEARER_TOKEN_BEDROCK
OPENAI_BASE_URL = "https://bedrock-mantle.us-east-2.api.aws/v1"

FLASK_ENV = "development"
FLASK_DEBUG = "True"

# ============================================================================
# Generate .env file (no need to modify)
# ============================================================================

env_content = f"""# IAM Chatbot Environment Variables
# OpenAI API Configuration
OPENAI_API_KEY={OPENAI_API_KEY}
OPENAI_BASE_URL={OPENAI_BASE_URL}

# Flask Configuration
FLASK_ENV={FLASK_ENV}
FLASK_DEBUG={FLASK_DEBUG}
"""

env_file = Path(__file__).parent / ".env"
env_file.write_text(env_content, encoding='utf-8')

print(".env file generated successfully")
print("")
print("You can now run:")
print("  python backend.py   # Start backend")
print("  python frontend.py  # Start frontend (in another terminal)")
