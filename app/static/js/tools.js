// Tools page logic: Code Assistant & Text Summarizer
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initCodeStudio();
  initSummarizer();
});

// Tab switching
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add('active');
    });
  });
}

// Code Studio Logic
function initCodeStudio() {
  const codeForm = document.getElementById('codeForm');
  const codeResult = document.getElementById('codeResult');
  const codeBtn = document.getElementById('runCodeBtn');
  const copyCodeBtn = document.getElementById('copyCodeResultBtn');

  if (!codeForm) return;

  codeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const code = document.getElementById('codeInput').value.trim();
    if (!code) {
      showToast('Please enter some code to process.', 'warning');
      return;
    }

    const action = document.getElementById('codeAction').value;
    const language = document.getElementById('codeLanguage').value;
    const model = document.getElementById('codeModelSelect').value;
    const apiKey = getActiveApiKey();

    codeBtn.disabled = true;
    codeBtn.innerHTML = '<span class="spinner"></span> Processing Code...';
    codeResult.innerHTML = '<p class="text-secondary">Gemini is analyzing your code...</p>';

    try {
      const res = await fetch('/api/code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code,
          action,
          language,
          model: model || null,
          api_key: apiKey || null
        })
      });

      const data = await res.json();
      codeBtn.disabled = false;
      codeBtn.innerHTML = '⚡ Run Code Tool';

      if (!res.ok) {
        const errorMsg = data.detail || 'Code processing failed.';
        codeResult.innerHTML = `<div class="toast toast-error" style="position:static;">${errorMsg}</div>`;
        showToast(errorMsg, 'error');
        return;
      }

      if (window.marked) {
        codeResult.innerHTML = window.marked.parse(data.result);
        if (window.hljs) {
          codeResult.querySelectorAll('pre code').forEach(block => window.hljs.highlightElement(block));
        }
      } else {
        codeResult.textContent = data.result;
      }
      if (copyCodeBtn) copyCodeBtn.style.display = 'inline-flex';
      showToast('Analysis completed!', 'success');
    } catch (err) {
      codeBtn.disabled = false;
      codeBtn.innerHTML = '⚡ Run Code Tool';
      codeResult.innerHTML = `<div class="toast toast-error" style="position:static;">Network error: ${err.message}</div>`;
    }
  });

  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(codeResult.innerText);
      showToast('Copied result to clipboard!', 'success');
    });
  }
}

// Summarizer Logic
function initSummarizer() {
  const sumForm = document.getElementById('summarizerForm');
  const sumResult = document.getElementById('sumResult');
  const sumBtn = document.getElementById('runSumBtn');
  const copySumBtn = document.getElementById('copySumResultBtn');

  if (!sumForm) return;

  sumForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('sumInput').value.trim();
    if (!text) {
      showToast('Please enter text to summarize.', 'warning');
      return;
    }

    const style = document.getElementById('sumStyle').value;
    const length = document.getElementById('sumLength').value;
    const model = document.getElementById('sumModelSelect').value;
    const apiKey = getActiveApiKey();

    sumBtn.disabled = true;
    sumBtn.innerHTML = '<span class="spinner"></span> Summarizing...';
    sumResult.innerHTML = '<p class="text-secondary">Synthesizing content...</p>';

    try {
      const res = await fetch('/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          style,
          length,
          model: model || null,
          api_key: apiKey || null
        })
      });

      const data = await res.json();
      sumBtn.disabled = false;
      sumBtn.innerHTML = '📝 Generate Summary';

      if (!res.ok) {
        const errorMsg = data.detail || 'Summarization failed.';
        sumResult.innerHTML = `<div class="toast toast-error" style="position:static;">${errorMsg}</div>`;
        showToast(errorMsg, 'error');
        return;
      }

      if (window.marked) {
        sumResult.innerHTML = window.marked.parse(data.summary);
      } else {
        sumResult.textContent = data.summary;
      }
      if (copySumBtn) copySumBtn.style.display = 'inline-flex';
      showToast('Summary generated!', 'success');
    } catch (err) {
      sumBtn.disabled = false;
      sumBtn.innerHTML = '📝 Generate Summary';
      sumResult.innerHTML = `<div class="toast toast-error" style="position:static;">Network error: ${err.message}</div>`;
    }
  });

  if (copySumBtn) {
    copySumBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(sumResult.innerText);
      showToast('Summary copied to clipboard!', 'success');
    });
  }
}
