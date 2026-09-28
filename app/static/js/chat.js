// Chat assistant page logic
let chatHistory = [];

const personas = {
  general: "You are a helpful, witty, and polite general AI assistant powered by Google Gemini.",
  python: "You are a senior Python architect and clean code advocate. Provide clean, type-annotated, idiomatic Python solutions.",
  writer: "You are an eloquent creative writer and copyeditor. Craft engaging, stylish prose with crisp storytelling.",
  analyst: "You are a precise data and logic analyst. Be concise, direct, and structured with bullet points and facts."
};

document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const clearChatBtn = document.getElementById('clearChatBtn');
  const exportChatBtn = document.getElementById('exportChatBtn');
  const personaSelect = document.getElementById('personaSelect');
  const customSystemPrompt = document.getElementById('customSystemPrompt');

  if (!chatForm) return;

  // Handle Enter to submit (Shift+Enter for newline)
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event('submit'));
    }
  });

  // Persona change
  if (personaSelect) {
    personaSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      if (val === 'custom') {
        customSystemPrompt.style.display = 'block';
      } else {
        customSystemPrompt.style.display = 'none';
        customSystemPrompt.value = personas[val] || '';
      }
    });
  }

  // Clear chat
  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', () => {
      if (confirm('Clear the conversation history?')) {
        chatHistory = [];
        const messagesDiv = document.getElementById('chatMessages');
        messagesDiv.innerHTML = `
          <div class="chat-bubble bot">
            <p>👋 Hello! I am your Gemini AI assistant. How can I help you today?</p>
          </div>
        `;
      }
    });
  }

  // Export chat
  if (exportChatBtn) {
    exportChatBtn.addEventListener('click', () => {
      if (chatHistory.length === 0) {
        showToast('No chat history to export.', 'info');
        return;
      }
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(chatHistory, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `gemini_chat_${Date.now()}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    });
  }

  // Chat submit
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    chatInput.value = '';
    appendMessage('user', message);
    chatHistory.push({ role: 'user', content: message });

    // Loading indicator
    const loadingId = appendLoadingBubble();

    // Determine system prompt
    let systemInstruction = "";
    if (personaSelect) {
      const selected = personaSelect.value;
      systemInstruction = selected === 'custom' ? customSystemPrompt.value : (personas[selected] || "");
    }

    const modelSelect = document.getElementById('modelSelect');
    const selectedModel = modelSelect ? modelSelect.value : null;
    const apiKey = getActiveApiKey();

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: chatHistory,
          system_instruction: systemInstruction,
          model: selectedModel,
          api_key: apiKey || null
        })
      });

      const data = await res.json();
      removeLoadingBubble(loadingId);

      if (!res.ok) {
        const errorMsg = data.detail || 'An error occurred while calling the Gemini API.';
        appendMessage('bot', `⚠️ **Error**: ${errorMsg}`);
        showToast(errorMsg, 'error');
        return;
      }

      appendMessage('bot', data.reply);
      chatHistory.push({ role: 'model', content: data.reply });
    } catch (err) {
      removeLoadingBubble(loadingId);
      appendMessage('bot', `⚠️ **Network Error**: Unable to reach server. ${err.message}`);
      showToast('Network error', 'error');
    }
  });
});

function appendMessage(role, content) {
  const messagesDiv = document.getElementById('chatMessages');
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role}`;

  if (window.marked && role === 'bot') {
    bubble.innerHTML = window.marked.parse(content);
    if (window.hljs) {
      bubble.querySelectorAll('pre code').forEach((block) => {
        window.hljs.highlightElement(block);
      });
    }
  } else {
    const p = document.createElement('p');
    p.textContent = content;
    bubble.appendChild(p);
  }

  messagesDiv.appendChild(bubble);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function appendLoadingBubble() {
  const messagesDiv = document.getElementById('chatMessages');
  const id = 'loading-' + Date.now();
  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble bot';
  bubble.id = id;
  bubble.innerHTML = `<span class="spinner" style="border-top-color: var(--accent-primary);"></span> Thinking...`;
  messagesDiv.appendChild(bubble);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  return id;
}

function removeLoadingBubble(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}
