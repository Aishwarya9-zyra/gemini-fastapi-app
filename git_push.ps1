# Push Gemini AI Hub to GitHub PowerShell Script
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "       Gemini AI Hub - Push Complete Package to GitHub" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git was not found in your PATH." -ForegroundColor Red
    Write-Host "Please install Git for Windows from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or install via Administrator terminal: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}

# 1. Initialize Git Repo
Write-Host "[1/5] Checking Git repository..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    git init -b main
} else {
    git branch -M main
}

# 2. Stage files
Write-Host "[2/5] Staging files (.env excluded via .gitignore)..." -ForegroundColor Cyan
git add .

# 3. Commit
Write-Host "[3/5] Creating commit..." -ForegroundColor Cyan
git commit -m "feat: complete Gemini AI Hub FastAPI application package"

# 4. Get GitHub Remote URL
Write-Host ""
$repoUrl = Read-Host "Enter your GitHub Repository URL (e.g. https://github.com/YOUR_USERNAME/gemini-fastapi-app.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "[ERROR] No URL provided. Aborted." -ForegroundColor Red
    exit 1
}

git remote remove origin 2>$null
git remote add origin $repoUrl

# 5. Push
Write-Host "[5/5] Pushing to GitHub (main branch)..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Project successfully published to GitHub." -ForegroundColor Green
    Write-Host "====================================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[NOTE] If the remote has conflicting commits, run:" -ForegroundColor Yellow
    Write-Host "  git pull origin main --rebase" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
}
