/**
 * YojanaMitra Global Chatbot JS
 * Automatically injects the chatbot UI and handles messaging logic.
 */

(function () {
    // 1. Inject CSS for portability
    const chatbotStyles = `
    .chat-toggle-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        z-index: 99999;
        cursor: pointer;
        font-size: 1.5rem;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .chat-toggle-btn:hover { transform: scale(1.1); box-shadow: 0 12px 40px rgba(59, 130, 246, 0.5); }
    .chatbox {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 350px;
        height: 450px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 1.5rem;
        box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.2);
        z-index: 99999;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .chat-header {
        background: #2563eb;
        color: white;
        padding: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
    }
    .chat-messages { flex-grow: 1; padding: 1.5rem; overflow-y: auto; background: #f8fafc; }
    .message { padding: 0.8rem 1rem; border-radius: 1rem; margin-bottom: 0.8rem; max-width: 85%; font-size: 0.9rem; line-height: 1.5; }
    .message.bot { background: white; color: #1e293b; border-bottom-left-radius: 0.25rem; margin-right: auto; border: 1px solid #e2e8f0; }
    .message.user { background: #2563eb; color: white; border-bottom-right-radius: 0.25rem; margin-left: auto; }
    .chat-input-area { padding: 1rem; border-top: 1px solid #e2e8f0; background: white; }
    `;

    const styleSheet = document.createElement("style");
    styleSheet.innerText = chatbotStyles;
    document.head.appendChild(styleSheet);

    // 2. Inject HTML
    const chatbotHTML = `
    <button class="chat-toggle-btn" onclick="toggleChat()" title="Ask YojanaMitra AI">
        <i class="fas fa-comment-dots"></i>
    </button>

    <div id="chatbox" class="chatbox" style="display:none;">
        <div class="chat-header">
            <span><i class="fas fa-headset me-2"></i>YojanaMitra Assistant</span>
            <button class="btn btn-sm btn-outline-light border-0" onclick="toggleChat()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="chat-messages" id="chat-messages">
            <div class="message bot">
                Hello! I can help you find schemes, explain eligibility, and answer your questions. How can I assist you today?
            </div>
        </div>
        <div class="chat-input-area">
            <div class="input-group">
                <input type="text" id="chat-input" class="form-control" placeholder="Type your message..." 
                    onkeypress="if(event.key==='Enter') sendChatMessage()">
                <button class="btn btn-primary" onclick="sendChatMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
            <small class="text-muted mt-1 d-block text-center" style="font-size: 10px;">Powered by Gemini AI</small>
        </div>
    </div>
    `;

    document.addEventListener('DOMContentLoaded', () => {
        const div = document.createElement('div');
        div.id = 'yojanmitra-chatbot-container';
        div.innerHTML = chatbotHTML;
        document.body.appendChild(div);
    });

    // --- Expose functions to window for HTML onclick handlers ---
    window.toggleChat = function () {
        const chatbox = document.getElementById('chatbox');
        if (!chatbox) return;
        chatbox.style.display = chatbox.style.display === 'none' ? 'flex' : 'none';
        if (chatbox.style.display === 'flex') {
            document.getElementById('chat-input').focus();
        }
    };

    window.sendChatMessage = async function () {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        input.value = '';

        const typingId = addMessage('Thinking...', 'bot');

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await res.json();

            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();

            addMessage(data.response, 'bot');
        } catch (e) {
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            addMessage('Error connecting to assistant.', 'bot');
        }
    };

    function addMessage(text, sender) {
        const container = document.getElementById('chat-messages');
        if (!container) return;

        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.textContent = text;
        div.id = 'msg-' + Date.now() + Math.random().toString(36).substr(2, 5);
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
        return div.id;
    }
})();
