from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.views import router as views_router, templates
from app.routes.api import router as api_router

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack AI workspace powered by FastAPI, Jinja2, and Google Gemini API."
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Mount Routers
app.include_router(views_router)
app.include_router(api_router)

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return {"detail": "Resource not found"}
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
            "has_api_key": bool(settings.GEMINI_API_KEY),
            "available_models": settings.AVAILABLE_MODELS,
            "default_model": settings.DEFAULT_MODEL,
            "error_message": "Page not found (404). Redirected to home."
        },
        status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
