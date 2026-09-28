// Main UI logic: Theme handling, global notifications, session API key support
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initApiStatus();
});

// Theme Management
function initTheme() {
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    themeToggle.setAttribute('title', `Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`);
  }
}

// Global Toast Notifications
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Retrieve API key from SessionStorage (if user entered one in Settings)
function getActiveApiKey() {
  return sessionStorage.getItem('gemini_api_key') || '';
}

// Update API Status badge dynamically
async function initApiStatus() {
  const badge = document.getElementById('apiStatusBadge');
  if (!badge) return;

  const sessionKey = getActiveApiKey();
  try {
    const res = await fetch('/api/health');
    const data = await res.json();

    if (data.has_server_key || (sessionKey && sessionKey.length > 5)) {
      badge.className = 'api-status-badge status-online';
      badge.innerHTML = '<span class="status-dot"></span> Gemini Ready';
    } else {
      badge.className = 'api-status-badge status-offline';
      badge.innerHTML = '<span class="status-dot"></span> Key Required';
    }
  } catch (err) {
    badge.className = 'api-status-badge status-offline';
    badge.innerHTML = '<span class="status-dot"></span> Disconnected';
  }
}
