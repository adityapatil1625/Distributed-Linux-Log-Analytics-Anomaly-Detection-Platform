#!/bin/bash
# Vercel Deployment Helper Script for Linux/Mac

echo ""
echo "========================================"
echo "Vercel Deployment Setup"
echo "Distributed Log Analytics"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed"
    exit 1
fi
echo "[OK] Git is installed"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "[WARNING] npm is not installed. Vercel CLI won't work."
    echo "Install from: https://nodejs.org"
else
    echo "[OK] npm is installed"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    exit 1
fi
echo "[OK] Python3 is installed"

echo ""
echo "Choose deployment method:"
echo ""
echo "1. Deploy with Vercel CLI"
echo "2. Deploy via GitHub"
echo "3. View deployment guide"
echo "4. Test API locally"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Installing Vercel CLI..."
        npm install -g vercel
        echo ""
        echo "Logging in to Vercel..."
        vercel login
        echo ""
        echo "Starting deployment..."
        vercel
        ;;
    2)
        echo ""
        echo "GitHub Deployment Steps:"
        echo ""
        echo "1. Make sure your project is committed:"
        echo "   git add ."
        echo "   git commit -m 'Setup for Vercel deployment'"
        echo ""
        echo "2. Push to GitHub"
        echo ""
        echo "3. Go to https://vercel.com/new"
        echo ""
        echo "4. Import your Git repository"
        echo ""
        echo "5. Vercel will auto-detect the configuration"
        echo ""
        echo "6. Click Deploy"
        echo ""
        ;;
    3)
        echo ""
        echo "Opening deployment guide..."
        if [ -f VERCEL_DEPLOYMENT.md ]; then
            less VERCEL_DEPLOYMENT.md
        else
            echo "File not found: VERCEL_DEPLOYMENT.md"
        fi
        ;;
    4)
        echo ""
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        echo ""
        echo "Starting local API server..."
        echo "Visit: http://localhost:8000"
        echo "API Docs: http://localhost:8000/docs"
        echo ""
        uvicorn api.main:app --reload
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
