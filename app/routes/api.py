import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Header
from pydantic import BaseModel, Field
from app.config import settings
from app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["API"])

# Request / Response Schemas
class MessageItem(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'model' / 'assistant'")
    content: str = Field(..., description="Text content of the message")

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    system_instruction: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    api_key: Optional[str] = None

class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1)
    action: str = Field(default="explain", description="explain, debug, optimize, test, refactor")
    language: Optional[str] = "python"
    model: Optional[str] = None
    api_key: Optional[str] = None

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=5)
    style: Optional[str] = "bullets"
    length: Optional[str] = "medium"
    model: Optional[str] = None
    api_key: Optional[str] = None

class VerifyKeyRequest(BaseModel):
    api_key: Optional[str] = None

class SaveKeyRequest(BaseModel):
    api_key: str

# Endpoints
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "models": settings.AVAILABLE_MODELS,
        "has_server_key": bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here")
    }

@router.post("/verify-key")
async def verify_key(payload: VerifyKeyRequest):
    key = (payload.api_key or "").strip() or settings.GEMINI_API_KEY.strip()
    if not key:
        return {"valid": False, "message": "No API key was provided or configured."}
    result = GeminiService.verify_api_key(key)
    return result

@router.post("/settings/save-key")
async def save_runtime_key(payload: SaveKeyRequest):
    clean_key = payload.api_key.strip()
    if not clean_key:
        raise HTTPException(status_code=400, detail="API key cannot be empty.")
    settings.GEMINI_API_KEY = clean_key
    return {"success": True, "message": "API key updated in application session successfully."}

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty.")
    
    try:
        messages_dicts = [m.model_dump() for m in payload.messages]
        reply = GeminiService.generate_chat_response(
            messages=messages_dicts,
            system_instruction=payload.system_instruction,
            model=payload.model,
            temperature=payload.temperature or 0.7,
            api_key=payload.api_key
        )
        return {"success": True, "reply": reply}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Chat generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

@router.post("/vision")
async def vision_endpoint(
    image: UploadFile = File(...),
    prompt: str = Form("Describe this image in detail"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None)
):
    valid_content_types = ["image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp"]
    if image.content_type not in valid_content_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type '{image.content_type}'. Supported: JPEG, PNG, WEBP, GIF, BMP."
        )

    try:
        image_bytes = await image.read()
        if len(image_bytes) > 20 * 1024 * 1024:  # 20MB limit
            raise HTTPException(status_code=400, detail="Image size exceeds 20MB limit.")

        analysis = GeminiService.analyze_image(
            image_bytes=image_bytes,
            mime_type=image.content_type,
            prompt=prompt,
            model=model,
            api_key=api_key
        )
        return {"success": True, "analysis": analysis}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Vision analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini Vision Error: {str(e)}")

@router.post("/code")
async def code_endpoint(payload: CodeRequest):
    try:
        result = GeminiService.process_code(
            code=payload.code,
            action=payload.action,
            language=payload.language or "python",
            model=payload.model,
            api_key=payload.api_key
        )
        return {"success": True, "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Code processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini Code Error: {str(e)}")

@router.post("/summarize")
async def summarize_endpoint(payload: SummarizeRequest):
    try:
        summary = GeminiService.summarize_text(
            text=payload.text,
            style=payload.style or "bullets",
            length=payload.length or "medium",
            model=payload.model,
            api_key=payload.api_key
        )
        return {"success": True, "summary": summary}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Gemini Summarize Error: {str(e)}")
