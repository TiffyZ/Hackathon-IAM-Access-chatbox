#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flask Backend - Simple Chatbot with LLM"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)


def call_llm(prompt: str, model_id: str = "openai.gpt-oss-120b") -> str:
    """Call LLM to generate response with fallback for SDK compatibility issues."""
    
    # Debug: Print current API Key information
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    print(f"\n=== Debug Info ===")
    print(f"API Key length: {len(api_key) if api_key else 'None'}")
    print(f"API Key first 100 chars: {api_key[:100] if api_key else 'None'}")
    print(f"Contains prefix: {'AWS_BEARER_TOKEN_BEDROCK=' in (api_key or '')}")
    print(f"Base URL: {base_url}")
    print(f"=============================\n")
    
    try:
        # Try OpenAI SDK first
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0
        )

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except TypeError as e:
        if "proxies" in str(e):
            # Fallback: use direct HTTP requests for SDK compatibility issues
            try:
                # Get token and clean it if needed
                token = os.environ.get('OPENAI_API_KEY')
                if token.startswith('AWS_BEARER_TOKEN_BEDROCK='):
                    token = token.replace('AWS_BEARER_TOKEN_BEDROCK=', '')
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500
                }
                response = requests.post(
                    f"{os.environ.get('OPENAI_BASE_URL')}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                # Check response status and content
                if response.status_code != 200:
                    response_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    raise Exception(f"API returned status {response.status_code}: {response_data}")
                
                response_json = response.json()
                if 'choices' not in response_json:
                    raise Exception(f"Invalid API response: 'choices' key not found. Response: {response_json}")
                
                return response_json['choices'][0]['message']['content'].strip()
            except requests.exceptions.RequestException as req_err:
                raise Exception(f"HTTP request failed: {str(req_err)}")
        else:
            raise Exception(f"LLM API call failed: {str(e)}")
    except Exception as e:
        raise Exception(f"LLM API call failed: {str(e)}")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chatbot requests"""
    try:
        data = request.json
        
        # Handle None data
        if data is None:
            return jsonify({"status": "error", "message": "Request body must be JSON"}), 400
        
        question = data.get("question") or ""
        question = question.strip() if isinstance(question, str) else ""

        if not question:
            return jsonify({"status": "error", "message": "Question cannot be empty"}), 400

        # Call LLM directly with the user's question
        answer = call_llm(question)

        return jsonify({
            "status": "success",
            "question": question,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
