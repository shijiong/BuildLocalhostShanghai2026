const form = document.getElementById('chat-form');
const answerEl = document.getElementById('answer');
const sendBtn = document.getElementById('send-btn');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const question = document.getElementById('question').value.trim();
  const modelChoice = document.getElementById('model_choice').value;
  const imageInput = document.getElementById('image');
  if (!question) return;

  const data = new FormData();
  data.append('question', question);
  data.append('model_choice', modelChoice);
  if (imageInput.files && imageInput.files[0]) {
    data.append('image', imageInput.files[0]);
  }

  answerEl.textContent = '';
  sendBtn.disabled = true;
  sendBtn.textContent = '分析中...';

  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      body: data,
    });

    if (!response.ok || !response.body) {
      throw new Error(`HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      answerEl.textContent += decoder.decode(value, { stream: true });
    }
  } catch (err) {
    answerEl.textContent = `请求失败: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = '发送';
  }
});
