import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_api_key():
    original_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = ""
    yield
    settings.GEMINI_API_KEY = original_key

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI + Google Gemini" in response.text

def test_chat_page():
    response = client.get("/chat")
    assert response.status_code == 200
    assert "chatMessages" in response.text
    assert "chatForm" in response.text

def test_vision_page():
    response = client.get("/vision")
    assert response.status_code == 200
    assert "dropzone" in response.text

def test_tools_page():
    response = client.get("/tools")
    assert response.status_code == 200
    assert "codeStudioTab" in response.text
    assert "summarizerTab" in response.text

def test_settings_page():
    response = client.get("/settings")
    assert response.status_code == 200
    assert "Google Gemini API Key" in response.text

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "gemini-2.5-flash" in data["models"]

def test_api_verify_key_empty():
    response = client.post("/api/verify-key", json={"api_key": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False

def test_api_save_key():
    response = client.post("/api/settings/save-key", json={"api_key": "test_fake_api_key_12345"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_api_save_key_empty():
    response = client.post("/api/settings/save-key", json={"api_key": "   "})
    assert response.status_code == 400

def test_api_chat_empty_messages():
    response = client.post("/api/chat", json={"messages": []})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_api_vision_invalid_mime():
    fake_txt = io.BytesIO(b"hello world text file")
    response = client.post(
        "/api/vision",
        files={"image": ("test.txt", fake_txt, "text/plain")},
        data={"prompt": "test"}
    )
    assert response.status_code == 400
    assert "Unsupported image type" in response.json()["detail"]

def test_api_code_missing_key():
    response = client.post(
        "/api/code",
        json={"code": "print('hello')", "action": "explain", "api_key": ""}
    )
    assert response.status_code == 400
    assert "Gemini API Key is not configured" in response.json()["detail"]

def test_api_summarize_missing_key():
    response = client.post(
        "/api/summarize",
        json={"text": "Long text to summarize for testing purposes", "style": "bullets", "api_key": ""}
    )
    assert response.status_code == 400
    assert "Gemini API Key is not configured" in response.json()["detail"]

def test_custom_404_handler():
    response = client.get("/non-existent-route-404")
    assert response.status_code == 404
