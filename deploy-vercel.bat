@echo off
REM Vercel Deployment Helper Script for Windows

echo.
echo ========================================
echo Vercel Deployment Setup for Distributed Log Analytics
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Node.js/npm is not installed
    echo You can still deploy via GitHub, but Vercel CLI is recommended
    echo Install from: https://nodejs.org
) else (
    echo [OK] npm is installed
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)
echo [OK] Python is installed

REM Display deployment options
echo.
echo Choose deployment method:
echo.
echo 1. Deploy with Vercel CLI (requires npm)
echo 2. Deploy via GitHub (push and import on vercel.com)
echo 3. View deployment guide
echo 4. Test API locally
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Installing Vercel CLI...
    npm install -g vercel
    echo.
    echo Logging in to Vercel...
    vercel login
    echo.
    echo Starting deployment...
    vercel
    pause
) else if "%choice%"=="2" (
    echo.
    echo GitHub Deployment Steps:
    echo.
    echo 1. Make sure your project is committed to git:
    echo    git add .
    echo    git commit -m "Setup for Vercel deployment"
    echo.
    echo 2. Push to GitHub (if not already done)
    echo.
    echo 3. Go to https://vercel.com/new
    echo.
    echo 4. Click "Import Git Repository"
    echo.
    echo 5. Select your repository
    echo.
    echo 6. Vercel will auto-detect the configuration
    echo.
    echo 7. Click "Deploy"
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo Opening deployment guide...
    if exist VERCEL_DEPLOYMENT.md (
        type VERCEL_DEPLOYMENT.md | more
    ) else (
        echo File not found: VERCEL_DEPLOYMENT.md
    )
    pause
) else if "%choice%"=="4" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Starting local API server...
    echo Visit: http://localhost:8000
    echo API Docs: http://localhost:8000/docs
    echo.
    uvicorn api.main:app --reload
) else if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Exiting...
    exit /b 1
)
