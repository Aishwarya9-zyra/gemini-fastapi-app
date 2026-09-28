# 🌟 Gemini AI Hub (FastAPI + Jinja2 + Google Gemini API)

A full-stack, production-grade web application powered by **Python 3.10+**, **FastAPI**, **Jinja2 HTML/CSS templating**, and the **Google Gemini API** (`google-genai` SDK).

---

## ✨ Features

- **💬 Interactive AI Chat**:
  - Multi-turn conversation history.
  - Persona presets: *Senior Python Architect*, *Eloquent Writer*, *Concise Analyst*, or *Custom System Prompt*.
  - Full Markdown rendering with syntax-highlighted code blocks (`highlight.js`) and one-click JSON chat export.
- **👁️ Multimodal Vision Analyzer**:
  - Drag-and-drop image upload (PNG, JPEG, WEBP, GIF).
  - Ask Gemini questions about diagrams, screenshots, infographics, and photos.
- **💻 Developer Code Studio**:
  - Step-by-step code explanation.
  - Bug detection and security edge-case audit.
  - Performance and complexity optimization.
  - Automated unit test generator.
- **📝 Content & Summarization Studio**:
  - Transform long articles, transcripts, and documents into executive briefs, bullet points, TL;DRs, or beginner guides.
- **⚙️ Dynamic API Key & Settings**:
  - Load API key from `.env` file or enter/test it dynamically in the web UI.
  - Real-time connection diagnostic tester.
- **🎨 Modern Dark & Light Mode UI**:
  - Polished glassmorphism styling, responsive layout, fluid CSS custom properties, and toast notifications.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Backend** | Python 3.10+ &amp; FastAPI | Asynchronous web framework &amp; REST APIs |
| **Server** | Uvicorn | High-performance ASGI server |
| **Templating** | Jinja2 | Dynamic HTML server-side rendering |
| **Frontend** | HTML5, CSS3, Vanilla JS | Modern responsive layout, glassmorphism, dark/light themes |
| **AI Integration** | Google GenAI SDK (`google-genai`) | Official Gemini 2.5 Flash, 2.5 Pro &amp; 1.5 models |
| **Testing** | Pytest &amp; HTTPX TestClient | Comprehensive automated route &amp; API validation |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed:
```powershell
python --version
```

### 2. Get a Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API key"**.
4. Copy the generated key.

### 3. Setup Environment
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```
Open `.env` and set your key:
```env
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
DEFAULT_MODEL=gemini-2.5-flash
PORT=8000
```
*(Alternatively, you can skip editing `.env` and paste your key directly in the web UI's **Settings** tab!)*

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Run the Application
You can start the server using any of these methods:

- **Using Python entrypoint**:
  ```powershell
  python run.py
  ```
- **Using Uvicorn directly**:
  ```powershell
  uvicorn app.main:app --reload --port 8000
  ```
- **Using Windows Batch script**: Double-click `run.bat`
- **Using PowerShell script**: Run `.\run.ps1`

Visit the application in your browser:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📁 Project Structure

```
gemini-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization, routers, error handling
│   ├── config.py            # Environment configuration & settings
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py# Google GenAI SDK wrapper (chat, vision, code, summarize)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── views.py         # Jinja2 template routes (/, /chat, /vision, /tools, /settings)
│   │   └── api.py           # REST endpoints (/api/chat, /api/vision, /api/code, etc.)
│   ├── templates/
│   │   ├── base.html        # Shared HTML5 shell with navbar, theme toggle, footer
│   │   ├── index.html       # Landing page dashboard
│   │   ├── chat.html        # Multi-turn chat assistant with personas
│   │   ├── vision.html      # Multimodal image upload and analysis
│   │   ├── tools.html       # Code studio and summarizer tabs
│   │   └── settings.html    # API key tester & model information
│   └── static/
│       ├── css/
│       │   └── style.css    # Responsive styles and dark/light variables
│       └── js/
│           ├── main.js      # Global UI handlers, theme toggle, toast alerts
│           ├── chat.js      # Chat logic, message history, export
│           ├── vision.js    # Drag-and-drop file upload & preview
│           └── tools.js     # Code execution & summarizer client logic
├── tests/
│   ├── __init__.py
│   └── test_routes.py       # Automated endpoint & template tests
├── .env.example             # Configuration environment template
├── requirements.txt         # Python package dependencies
├── README.md                # Documentation & instructions
├── run.bat                  # One-click Windows CMD runner
├── run.ps1                  # PowerShell runner
└── run.py                   # Python Uvicorn runner
```

---

## 🧪 Running Automated Tests

Run the test suite with `pytest`:
```powershell
pytest tests/ -v
```

All 11 endpoint and template tests will validate template rendering, API health status, input validation, and 404 handling.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web dashboard |
| `GET` | `/chat` | Chat interface |
| `GET` | `/vision` | Multimodal vision analyzer |
| `GET` | `/tools` | Code &amp; summarizer studio |
| `GET` | `/settings` | Settings &amp; API credentials manager |
| `GET` | `/api/health` | Service health status and supported models |
| `POST` | `/api/verify-key` | Verify Gemini API credentials |
| `POST` | `/api/chat` | Send conversational turn |
| `POST` | `/api/vision` | Submit image multipart form for visual analysis |
| `POST` | `/api/code` | Explain, debug, optimize, test, or refactor code |
| `POST` | `/api/summarize` | Summarize long texts in selected style and length |

Interactive OpenAPI documentation is also automatically available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
