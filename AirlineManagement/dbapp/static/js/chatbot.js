// static/js/chatbot.js

document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chatWindow');
    const chatBody = document.getElementById('chatBody');

    // 1. Persistence: Restore window state
    if (sessionStorage.getItem('ba_chat_open') === 'true') {
        chatWindow.style.display = 'flex';
    }

    // 2. Persistence: Restore History
    const history = JSON.parse(sessionStorage.getItem('ba_chat_history')) || [];
    if (history.length > 0) {
        chatBody.innerHTML = '';
        history.forEach(m => renderMsg(m.text, m.type, m.replies, false));
    } else {
        autoGreet(); // Start fresh
    }

    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') userSend();
    });
});

function toggleChat() {
    const chat = document.getElementById('chatWindow');
    const isVisible = chat.style.display === 'flex';
    chat.style.display = isVisible ? 'none' : 'flex';
    sessionStorage.setItem('ba_chat_open', !isVisible);
}

function renderMsg(text, type, replies = [], isNew = true) {
    const body = document.getElementById('chatBody');
    removeTyping();
    const div = document.createElement('div');
    div.className = `msg ${type} shadow-sm`;
    div.innerHTML = text.replace(/\n/g, '<br>');
    
    if (replies.length > 0) {
        const qr = document.createElement('div');
        qr.className = "quick-replies mt-2";
        replies.forEach(r => {
            const btn = document.createElement('button');
            btn.className = "qr-btn";
            btn.innerText = r;
            btn.onclick = () => userSend(r);
            qr.appendChild(btn);
        });
        div.appendChild(qr);
    }
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;

    if (isNew) {
        let history = JSON.parse(sessionStorage.getItem('ba_chat_history')) || [];
        history.push({ text, type, replies });
        if (history.length > 15) history.shift();
        sessionStorage.setItem('ba_chat_history', JSON.stringify(history));
    }
}

// UPDATED: autoGreet now fetches data silently without rendering a user bubble
async function autoGreet() {
    showTyping();
    try {
        const resp = await fetch('/chatbot/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: 'hello' }) 
        });
        const data = await resp.json();
        // Render only the bot's response
        renderMsg(data.text, 'bot', data.quick_replies);
    } catch (e) {
        console.error("Greeting failed", e);
    }
}

async function userSend(manualMsg = null) {
    const input = document.getElementById('chatInput');
    const text = manualMsg || input.value.trim();
    if (!text) return;

    const navs = {
        "Login Now": ["/login", "Redirecting... You can login here with your credentials 🔐"],
        "Register": ["/register", "Redirecting... You can create your account here ✈️"],
        "Search Flights": ["/", "Going to search... You can find flights from the main bar."],
        "Book Now": ["/", "Please select a flight to begin booking."],
        "Main Menu": ["/", "Returning to Home..."]
    };

    renderMsg(text, 'user');

    if (navs[text]) {
        renderMsg(navs[text][1], 'bot', []);
        setTimeout(() => { window.location.href = navs[text][0]; }, 1000);
        return;
    }

    if (!manualMsg) input.value = '';
    showTyping();

    try {
        const resp = await fetch('/chatbot/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await resp.json();
        setTimeout(() => renderMsg(data.text, 'bot', data.quick_replies), 600);
    } catch (e) {
        renderMsg("System error. Try later.", "bot");
    }
}

function showTyping() {
    removeTyping();
    const body = document.getElementById('chatBody');
    const div = document.createElement('div');
    div.id = "typing"; div.className = "msg bot text-muted italic";
    div.innerHTML = "BoundlessAI is thinking...";
    body.appendChild(div);
}

function removeTyping() { const old = document.getElementById('typing'); if (old) old.remove(); }

function resetChat() { sessionStorage.removeItem('ba_chat_history'); location.reload(); }