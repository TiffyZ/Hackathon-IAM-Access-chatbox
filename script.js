// API Configuration - Using CORS proxy to bypass cross-origin restrictions
const API_URL = "https://cors-anywhere.herokuapp.com/http://54.234.0.211:5000/query";

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

// Show 2-second loading animation and load greeting on page load
window.addEventListener("load", () => {
    // Load greeting messages
    loadGreeting();
    
    // Show 2-second loading animation
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
        // Add context "(I'm Sarah Lee)" to the message
        const promptWithContext = `${message} (I'm Sarah Lee)`;
        
        console.log("Sending request to:", API_URL);
        console.log("Request body:", { query: promptWithContext });
        
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: promptWithContext }),
        });

        console.log("Response status:", response.status);
        console.log("Response headers:", response.headers);
        
        const data = await response.json();
        console.log("Response data:", data);

        if (response.ok) {
            // Handle response - check for explanation + data table format
            let messageHTML = "";
            
            if (data.explanation) {
                messageHTML += `<div>${data.explanation}</div>`;
            }
            
            if (data.data && Array.isArray(data.data) && data.data.length > 0) {
                // Generate HTML table from data array, exclude email column
                let headers = Object.keys(data.data[0]);
                headers = headers.filter(h => h !== "email");  // Exclude email column
                
                messageHTML += `
                    <table style="border-collapse: collapse; margin-top: 10px; width: 100%;">
                        <thead style="background-color: #f0f0f0;">
                            <tr>
                                ${headers.map(h => `<th style="border: 1px solid #ddd; padding: 6px; text-align: left; font-size: 12px;">${h}</th>`).join("")}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.data.map(row => `
                                <tr>
                                    ${headers.map(h => `<td style="border: 1px solid #ddd; padding: 6px; font-size: 12px;">${row[h]}</td>`).join("")}
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                `;
            }
            
            // Fallback if no explanation or data
            if (!messageHTML) {
                messageHTML = data.answer || data.response || data.result || data.output || JSON.stringify(data);
            }
            
            addMessage(messageHTML, "assistant", !!data.data);
        } else {
            // Add error message
            addMessage(`Error: ${data.message || response.statusText || "Unknown error"}`, "assistant");
        }
    } catch (error) {
        console.error("Fetch error:", error);
        console.error("Error message:", error.message);
        
        // More specific error messages
        if (error.message.includes("Failed to fetch")) {
            addMessage("Network error: Cannot reach the server. This may be a CORS issue or the server is offline.", "assistant");
        } else {
            addMessage(`Error: ${error.message}`, "assistant");
        }
    } finally {
        loading.classList.remove("active");
        sendBtn.disabled = false;
        chatInput.focus();
    }
}

function addMessage(text, sender, isHTML = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    if (isHTML && text.includes("<table")) {
        // Separate explanation and table
        const explanationMatch = text.match(/<div>(.*?)<\/div>/s);
        const tableMatch = text.match(/<table[\s\S]*<\/table>/);
        
        if (explanationMatch) {
            const explanationDiv = document.createElement("p");
            explanationDiv.textContent = explanationMatch[1].trim();
            explanationDiv.style.whiteSpace = "pre-wrap";
            messageDiv.appendChild(explanationDiv);
        }
        
        if (tableMatch) {
            const tableContainer = document.createElement("div");
            tableContainer.className = "table-container";
            tableContainer.innerHTML = tableMatch[0];
            messageDiv.appendChild(tableContainer);
        }
    } else {
        const p = document.createElement("p");
        
        if (isHTML) {
            p.innerHTML = text;
        } else {
            p.textContent = text;
        }
        
        p.style.whiteSpace = "pre-wrap";
        messageDiv.appendChild(p);
    }

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

// Load initial messages on page startup
function loadGreeting() {
    console.log("Loading initial messages...");
    
    // Message 1: Greeting with date
    addMessage("Hello Sarah Lee! I hope you're having a wonderful Thursday, March 19, 2026. 🌞", "assistant");
    
    // Message 2: Warning
    addMessage("⚠️ Warning:\n You have 1 account is about to expire soon.", "assistant");
    
    console.log("Initial messages added successfully");
}
