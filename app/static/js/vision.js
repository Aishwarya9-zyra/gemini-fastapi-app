// Vision & multimodal analysis logic
document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('imageFileInput');
  const previewImg = document.getElementById('imagePreview');
  const previewContainer = document.getElementById('previewContainer');
  const visionForm = document.getElementById('visionForm');
  const visionResult = document.getElementById('visionResult');
  const visionBtn = document.getElementById('analyzeBtn');

  if (!dropzone || !fileInput) return;

  // Click to browse
  dropzone.addEventListener('click', () => fileInput.click());

  // Drag and drop events
  ['dragenter', 'dragover'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      fileInput.files = e.dataTransfer.files;
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  });

  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      showToast('Please select a valid image file (PNG, JPG, WEBP, GIF).', 'error');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      previewContainer.style.display = 'block';
      document.getElementById('fileNameBadge').textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    };
    reader.readAsDataURL(file);
  }

  // Vision Form Submit
  visionForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!fileInput.files || !fileInput.files[0]) {
      showToast('Please choose or drop an image first.', 'warning');
      return;
    }

    const promptText = document.getElementById('visionPrompt').value.trim();
    const modelSelect = document.getElementById('visionModelSelect');
    const selectedModel = modelSelect ? modelSelect.value : null;
    const apiKey = getActiveApiKey();

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('prompt', promptText || 'Analyze and describe this image in detail.');
    if (selectedModel) formData.append('model', selectedModel);
    if (apiKey) formData.append('api_key', apiKey);

    // Set loading state
    visionBtn.disabled = true;
    visionBtn.innerHTML = '<span class="spinner"></span> Analyzing Image...';
    visionResult.innerHTML = '<p class="text-secondary">Gemini is inspecting the image...</p>';

    try {
      const res = await fetch('/api/vision', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      visionBtn.disabled = false;
      visionBtn.innerHTML = '✨ Analyze Image';

      if (!res.ok) {
        const errorMsg = data.detail || 'Failed to analyze image.';
        visionResult.innerHTML = `<div class="toast toast-error" style="position:static;">${errorMsg}</div>`;
        showToast(errorMsg, 'error');
        return;
      }

      if (window.marked) {
        visionResult.innerHTML = window.marked.parse(data.analysis);
        if (window.hljs) {
          visionResult.querySelectorAll('pre code').forEach((block) => window.hljs.highlightElement(block));
        }
      } else {
        visionResult.textContent = data.analysis;
      }
      showToast('Analysis completed!', 'success');
    } catch (err) {
      visionBtn.disabled = false;
      visionBtn.innerHTML = '✨ Analyze Image';
      visionResult.innerHTML = `<p class="toast toast-error" style="position:static;">Network error: ${err.message}</p>`;
      showToast('Network error', 'error');
    }
  });
});
