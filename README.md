# IAM Chatbot

A lightweight, beautiful chatbot interface powered by AWS Bedrock LLM.

## Features

✨ **Floating Chat Button** - Minimize/open dialog from bottom-right corner  
💬 **Real-time Chat** - Smooth conversational interface  
🔔 **Notification Badge** - Red dot alerts for new messages  
🎨 **Elegant Design** - Beautiful gradient UI with animations  
🚀 **Cloud-Powered** - AWS Bedrock backend for intelligent responses  
📱 **Responsive** - Works on desktop, tablet, and mobile  

## Quick Start (2 Steps)

### Step 1: Configure AWS Token

Edit `configure.py` and set your AWS Bedrock token:

```python
AWS_BEARER_TOKEN_BEDROCK = "your_token_here"
```

Then run:
```bash
python configure.py
```

### Step 2: Start Services

**Terminal 1 - Backend:**
```bash
python backend.py
```

**Terminal 2 - Frontend:**
```bash
python frontend.py
```

Open `http://localhost:8000` - the chatbot loads automatically! 🎉

## File Structure

```
.
├── configure.py       # Configuration (set AWS token here)
├── backend.py         # Flask API server
├── frontend.py        # HTTP server for frontend
├── app.py            # Core Flask application
├── index.html        # Chat interface
├── style.css         # Styling & animations
├── script.js         # Chat logic & interactions
├── .env              # Environment variables (auto-generated)
└── README.md         # This file
```

## How It Works

1. Click the purple chat button in the bottom-right corner
2. Type your question in the input box
3. Press Enter or click Send
4. Get an AI-powered response from AWS Bedrock
5. New messages trigger a red notification badge

## Customization

### Change Username
Edit `script.js`:
```javascript
const DEFAULT_USER = "Your Name";
```

### Change Greeting Prompt
Edit the `greetingPrompt` in `script.js` line ~127

### Adjust Colors
Edit `style.css`:
- Button: `.chatbot-button` (background gradient)
- Notification: `.notification-badge` (background-color)
- Messages: `.user-message` / `.assistant-message`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check if port 5000 is available; set FLASK_DEBUG=True |
| Frontend won't load | Ensure frontend.py is running on port 8000 |
| AWS API errors | Verify token in .env file; check AWS region |
| Chat not responding | Open browser console (F12) to see error messages |

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.13, Flask, Flask-CORS
- **LLM**: AWS Bedrock API with OpenAI SDK compatibility

## License

See LICENSE file
