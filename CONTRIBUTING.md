# Contributing to Gemini AI Hub

Thank you for your interest in contributing to **Gemini AI Hub**! We welcome bug reports, feature requests, and code contributions.

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/gemini-fastapi-app.git
   cd gemini-fastapi-app
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Add your Gemini API Key in `.env`.

5. **Run the Development Server**
   ```bash
   python run.py
   ```

---

## 🧪 Running Tests

Ensure all tests pass before submitting a pull request:
```bash
pytest tests/ -v
```

---

## 📜 Pull Request Guidelines

1. Create a feature branch: `git checkout -b feature/my-new-feature`
2. Follow PEP 8 style conventions for Python code.
3. Add unit tests for any new routes, endpoints, or services.
4. Ensure `.env` is never committed.
5. Push to your branch and open a Pull Request!
