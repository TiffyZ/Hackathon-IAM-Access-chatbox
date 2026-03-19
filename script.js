// API Configuration
const API_URL = "http://127.0.0.1:5000/api/chat";

// DOM Elements
const chatbotBtn = document.getElementById("chatbotBtn");
const closeBtn = document.getElementById("closeBtn");
const chatbotContainer = document.getElementById("chatbotContainer");
const messagesContainer = document.getElementById("messagesContainer");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const loading = document.getElementById("loading");
const notificationBadge = document.getElementById("notificationBadge");

// State
let isOpen = false;

// Show 2-second loading animation on page load
window.addEventListener("load", () => {
    chatbotBtn.classList.add("loading");
    setTimeout(() => {
        chatbotBtn.classList.remove("loading");
    }, 2000);
});

// open/close chatbot
chatbotBtn.addEventListener("click", () => {
    if (isOpen) {
        closeChatbot();
    } else {
        openChatbot();
    }
});

function openChatbot() {
    chatbotContainer.classList.add("active");
    isOpen = true;
    chatInput.focus();
    // Hide notification badge when opening
    notificationBadge.classList.remove("show");
}

function closeChatbot() {
    chatbotContainer.classList.remove("active");
    isOpen = false;
}

closeBtn.addEventListener("click", closeChatbot);

// Send message
sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        sendMessage();
    }
});

async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) {
        alert("Please enter a question");
        return;
    }

    // Add user message
    addMessage(message, "user");
    chatInput.value = "";

    // Show loading state
    loading.classList.add("active");
    sendBtn.disabled = true;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question: message }),
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            // Add assistant response
            addMessage(data.answer, "assistant");
        } else {
            // Add error message
            addMessage(`Error: ${data.message || "Unknown error"}`, "assistant");
        }
    } catch (error) {
        console.error("Error:", error);
        addMessage(`Network error: ${error.message}`, "assistant");
    } finally {
        loading.classList.remove("active");
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    const p = document.createElement("p");
    p.textContent = text;

    messageDiv.appendChild(p);
    messagesContainer.appendChild(messageDiv);

    // Auto scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Show notification badge when receiving new message and chatbot is not open
    if (sender === "assistant" && !isOpen) {
        notificationBadge.classList.add("show");
    }
}

// User configuration
const DEFAULT_USER = "Sarah Lee";

// Load greeting on page startup
async function loadGreeting() {
    console.log("Loading greeting...");
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const greetingPrompt = `User: Sarah Lee\nToday's date: ${today}\n\nGenerate a friendly, warm greeting message for the user that includes today's date. Keep it brief (1-2 sentences). Be professional but personable.`;
    
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question: greetingPrompt }),
        });

        const data = await response.json();
        console.log("Greeting response:", data);

        if (response.ok && data.status === "success") {
            // Add assistant greeting (no user message shown)
            addMessage(data.answer, "assistant");
            console.log("Greeting added successfully");
        } else {
            // Fallback greeting if API fails
            console.error("API error, using fallback");
            addMessage("Hello! I'm ready to help you. How can I assist?", "assistant");
        }
    } catch (error) {
        console.error("Error loading greeting:", error);
        // Fallback greeting if network fails
        addMessage("Hello! I'm ready to help you. How can I assist?", "assistant");
    }
}

// Page load - load greeting immediately
console.log("Script loaded, attempting to load greeting...");
loadGreeting();
