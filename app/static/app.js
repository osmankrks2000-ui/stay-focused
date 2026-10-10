const form = document.getElementById('leadForm');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
      const r = await fetch('/api/leads', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      const d = await r.json();
      document.getElementById('formMsg').textContent = d.message || d.error || 'İşlem tamamlanamadı.';
      if (d.success) form.reset();
    } catch {
      document.getElementById('formMsg').textContent = 'Sunucuya bağlanılamadı.';
    }
  });
}

const chatHistory = [];
async function sendChat() {
  const input = document.getElementById('chatInput');
  const log = document.getElementById('chatLog');
  if (!input || !log) return;
  const msg = input.value.trim();
  if (!msg) return;

  appendChatMessage('user', msg);
  chatHistory.push({role: 'user', content: msg});
  input.value = '';
  input.disabled = true;

  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg, history: chatHistory.slice(-10, -1)})
    });
    const d = await r.json();
    const answer = d.answer || d.error || 'Bir hata oluştu.';
    appendChatMessage('bot', answer);
    if (d.success) chatHistory.push({role: 'assistant', content: answer});
  } catch {
    appendChatMessage('bot', 'Sunucuya bağlanılamadı. Lütfen tekrar deneyin.');
  } finally {
    input.disabled = false;
    input.focus();
  }
}

function appendChatMessage(type, text) {
  const log = document.getElementById('chatLog');
  const item = document.createElement('div');
  item.className = type;
  item.textContent = text; // Kullanıcı/model metni HTML olarak çalıştırılmaz.
  log.appendChild(item);
  log.scrollTop = log.scrollHeight;
}

const chatInput = document.getElementById('chatInput');
if (chatInput) {
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendChat();
    }
  });
}
