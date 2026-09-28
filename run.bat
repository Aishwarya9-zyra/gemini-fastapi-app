@echo off
title Gemini AI Hub - FastAPI App
echo =========================================================
echo       Starting Gemini AI Hub (FastAPI + Jinja2)
echo =========================================================

REM Check Python command
where python >nul 2>nul
if %errorlevel% equ 0 (
    python run.py
) else (
    if exist "C:\Users\AIDS\anaconda3\python.exe" (
        "C:\Users\AIDS\anaconda3\python.exe" run.py
    ) else (
        echo [ERROR] Python not found in PATH or at C:\Users\AIDS\anaconda3\python.exe!
        echo Please ensure Python 3.10+ is installed.
        pause
    )
)
pause
