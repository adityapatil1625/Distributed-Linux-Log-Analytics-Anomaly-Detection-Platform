# 🚀 Vercel Deployment - Quick Start Guide

## 3-Step Deployment

### Step 1: Prepare (2 minutes)
```powershell
# Navigate to project
cd C:\Users\adity\Downloads\distributed-log-analytics

# Commit changes
git add .
git commit -m "Setup for Vercel deployment"
```

### Step 2: Deploy (Choose One)

#### Option A: Vercel CLI (Fastest)
```powershell
# Install Vercel CLI (one time only)
npm install -g vercel

# Login to your Vercel account
vercel login

# Deploy
vercel
# Follow prompts, accept defaults
```

#### Option B: GitHub (Easiest for teams)
```powershell
# Push to GitHub
git push origin main

# Go to https://vercel.com/new
# Import repository → Deploy (auto-detected)
```

#### Option C: Helper Script
```powershell
# Windows
.\deploy-vercel.bat
# Select option 1 or 4
```

### Step 3: Verify
Once deployed, you'll get a URL like `https://your-project.vercel.app`

Visit these in your browser:
- `https://your-project.vercel.app/` - Root endpoint
- `https://your-project.vercel.app/docs` - Interactive API explorer
- `https://your-project.vercel.app/health` - Health check

## Testing Commands

```powershell
# Replace with your actual Vercel URL
$url = "https://your-project.vercel.app"

# Test root
curl "$url/"

# Test health
curl "$url/health"

# Test API info
curl "$url/api/info"

# Test search logs
curl "$url/api/logs/search?query=error"

# Test get metrics
curl "$url/api/metrics"

# Test get alerts
curl "$url/api/alerts"
```

## Configuration

Add these environment variables in Vercel dashboard:
1. Go to Project Settings → Environment Variables
2. Add each variable:
   - `LOG_RETENTION_DAYS` = `30`
   - `MAX_LOG_SIZE_MB` = `100`
   - `ENABLE_ANOMALY_DETECTION` = `true`
   - `API_TIMEOUT_SECONDS` = `30`

## Local Testing (Before Deployment)

```powershell
# Fix virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.main:app --reload

# Open browser to http://localhost:8000/docs
```

## Project Structure

```
api/                    ← FastAPI app (deploys to Vercel)
├── main.py            ← All endpoints here
├── logs.py            ← Log routes
├── metrics.py         ← Metrics routes
├── alerts.py          ← Alerts routes
└── index.py           ← Root handler

vercel.json            ← Vercel config
requirements.txt       ← Python dependencies
VERCEL_DEPLOYMENT.md   ← Full deployment guide
```

## Available Endpoints After Deployment

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Root status |
| GET | `/health` | Health check |
| GET | `/api/info` | API information |
| GET | `/api/logs/search` | Search logs |
| GET | `/api/logs/stats` | Log statistics |
| POST | `/api/logs/ingest` | Add log |
| GET | `/api/metrics` | Current metrics |
| GET | `/api/metrics/history` | Metrics history |
| POST | `/api/metrics/record` | Record metric |
| GET | `/api/alerts` | List alerts |
| POST | `/api/alerts` | Create alert |
| DELETE | `/api/alerts/{id}` | Dismiss alert |

## Troubleshooting

### Build Failed
- Check `requirements.txt` is in root directory ✓
- Ensure all dependencies are listed ✓
- Verify `vercel.json` is correct ✓

### 502 Bad Gateway
- Check logs in Vercel dashboard
- Run locally to test: `uvicorn api.main:app --reload`
- Verify FastAPI version in requirements.txt

### Cold Start Slow
- Normal on Vercel's free tier (1-3 seconds)
- Upgrade to Pro plan for faster cold starts
- Disable unused features in `api/main.py`

### CORS Issues
- Already enabled for all origins in `api/main.py`
- Modify in main.py if needed

## What's Deployed

✅ **FastAPI HTTP API** - Vercel serverless functions  
✅ **All endpoints** - Logs, metrics, alerts, health checks  
✅ **Documentation** - Auto-generated at `/docs`  
✅ **CORS enabled** - Works with any frontend  

⚠️ **NOT deployed** (separate services needed):
- Log agents (agent/)
- TCP server (ingestion/)
- Anomaly detection (anomaly/)
- Dashboard/frontend (dashboard/)

## Next: Deploy Agents (Optional)

Your agents need separate hosting. Options:

- **Railway.app** - Easiest, similar to Vercel
- **Render.com** - Good alternative
- **Docker + Cloud Run/EC2** - More control

See `VERCEL_DEPLOYMENT.md` for details.

## Support

- 📖 [Full Deployment Guide](VERCEL_DEPLOYMENT.md)
- 📚 [FastAPI Docs](https://fastapi.tiangolo.com)
- 🔗 [Vercel Docs](https://vercel.com/docs)
- 💬 [Vercel Community](https://vercel.com/support)

---

**That's it!** Your project is ready to deploy. Choose a method above and follow the steps. 🎉
