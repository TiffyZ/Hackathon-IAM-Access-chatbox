#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IAM Chatbot - Streamlit Frontend"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="IAM Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# API Configuration
API_URL = "http://54.234.0.211:5000/query"

# Custom CSS
st.markdown("""
<style>
    .main {
        max-width: 900px;
    }
    .chat-message {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        display: flex;
        gap: 10px;
    }
    .user-message {
        background-color: #e8f5e9;
        flex-direction: row-reverse;
    }
    .bot-message {
        background-color: #e3f2fd;
        flex-direction: row;
    }
    .message-content {
        flex-grow: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Load greeting
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm your IAM Assistant. How can I help you today?\n\nYou can ask me about:\n- Who reports to me?\n- Access levels\n- Team information\n- And more...",
        "timestamp": datetime.now()
    })

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🤖")
with col2:
    st.markdown("### IAM Assistant")
    st.markdown("**User: Sarah Lee**")

st.divider()

# Chat messages
messages_container = st.container()

with messages_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <b>You:</b><br/>{message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-content">
                    <b>Assistant:</b><br/>{message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# Input area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Ask a question...",
        placeholder="e.g., Who reports to me?",
        key="user_input_field",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle message sending
if send_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now()
    })
    
    # Show loading state
    with st.spinner("Getting response..."):
        try:
            # Add context to the message (same as original)
            prompt_with_context = f"{user_input} (I'm Sarah Lee)"
            
            # Make API request
            response = requests.post(
                API_URL,
                json={"query": prompt_with_context},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse response
                if isinstance(data, dict):
                    # If response has explanation and data
                    if "explanation" in data:
                        message_content = data["explanation"]
                        if "data" in data and data["data"]:
                            message_content += "\n\n**Raw Data:**\n```json\n"
                            message_content += json.dumps(data["data"], indent=2)
                            message_content += "\n```"
                    else:
                        message_content = json.dumps(data, indent=2, ensure_ascii=False)
                else:
                    message_content = str(data)
            else:
                message_content = f"❌ Error: {response.status_code}\n{response.text}"
        
        except requests.exceptions.Timeout:
            message_content = "❌ Request timeout. Please try again."
        except requests.exceptions.ConnectionError:
            message_content = "❌ Connection error. Please check if the API is available."
        except Exception as e:
            message_content = f"❌ Error: {str(e)}"
    
    # Add bot response to chat
    st.session_state.messages.append({
        "role": "assistant",
        "content": message_content,
        "timestamp": datetime.now()
    })
    
    # Rerun to update chat display
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "IAM Access Chatbot | Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
)
