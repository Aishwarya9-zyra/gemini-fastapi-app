@echo off
setlocal enabledelayedexpansion
title Push Gemini AI Hub to GitHub
echo ====================================================================
echo        Gemini AI Hub - Push Complete Package to GitHub
echo ====================================================================
echo.

REM 1. Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not found in your PATH.
    echo.
    echo Please install Git for Windows from:
    echo https://git-scm.com/download/win
    echo or run in an Administrator terminal:
    echo winget install Git.Git
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking Git repository status...
if not exist ".git" (
    echo Initializing fresh Git repository on branch 'main'...
    git init -b main
) else (
    echo Existing Git repository found.
    git branch -M main
)

echo.
echo [2/5] Staging project files (.env is protected by .gitignore)...
git add .

echo.
echo [3/5] Creating initial commit...
git commit -m "feat: complete Gemini AI Hub FastAPI application package"

echo.
echo [4/5] Configure GitHub Remote:
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/YOUR_USERNAME/gemini-fastapi-app.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL entered. Aborting push.
    pause
    exit /b 1
)

git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo [5/5] Pushing to GitHub (main branch)...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ====================================================================
    echo   SUCCESS! Your project has been pushed to GitHub successfully.
    echo ====================================================================
) else (
    echo.
    echo [NOTE] Push failed. If the repository already has commits (like a README or license),
    echo you can try running:
    echo   git pull origin main --rebase
    echo   git push -u origin main
)

echo.
pause
