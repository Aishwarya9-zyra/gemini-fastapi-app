from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.config import settings

router = APIRouter()

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

def get_base_context(request: Request) -> dict:
    has_key = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here")
    return {
        "request": request,
        "app_name": settings.APP_NAME,
        "available_models": settings.AVAILABLE_MODELS,
        "default_model": settings.DEFAULT_MODEL,
        "has_api_key": has_key,
    }

@router.get("/", name="home")
async def home(request: Request):
    ctx = get_base_context(request)
    ctx["active_page"] = "home"
    return templates.TemplateResponse(request=request, name="index.html", context=ctx)

@router.get("/chat", name="chat")
async def chat_page(request: Request):
    ctx = get_base_context(request)
    ctx["active_page"] = "chat"
    return templates.TemplateResponse(request=request, name="chat.html", context=ctx)

@router.get("/vision", name="vision")
async def vision_page(request: Request):
    ctx = get_base_context(request)
    ctx["active_page"] = "vision"
    return templates.TemplateResponse(request=request, name="vision.html", context=ctx)

@router.get("/tools", name="tools")
async def tools_page(request: Request):
    ctx = get_base_context(request)
    ctx["active_page"] = "tools"
    return templates.TemplateResponse(request=request, name="tools.html", context=ctx)

@router.get("/settings", name="settings")
async def settings_page(request: Request):
    ctx = get_base_context(request)
    ctx["active_page"] = "settings"
    return templates.TemplateResponse(request=request, name="settings.html", context=ctx)
