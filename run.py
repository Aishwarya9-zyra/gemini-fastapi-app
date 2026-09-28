#!/usr/bin/env python3
"""
Entrypoint to run the Gemini AI Hub application.
Usage:
    python run.py
"""
import sys
import uvicorn
from app.config import settings

def main():
    print("=" * 60)
    print(f"  Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"  URL: http://{settings.HOST}:{settings.PORT}")
    print(f"  Gemini API Key configured: {'Yes' if settings.GEMINI_API_KEY else 'No (set via Settings UI)'}")
    print("=" * 60)

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    main()
