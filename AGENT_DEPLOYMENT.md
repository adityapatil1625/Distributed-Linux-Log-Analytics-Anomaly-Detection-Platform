# Complete Agent Deployment Guide

This guide covers deploying the enhanced distributed agents to Railway.app and Render.com for production use.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Vercel API                          │
│  https://your-app.vercel.app  (FastAPI + Dashboard)        │
└─────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
    Send Logs             Send Metrics         Send Alerts
         │                    │                    │
    ┌────┴────┐          ┌────┴────┐         ┌────┴────┐
    │  Log     │          │ Metrics  │         │ Anomaly  │
    │ Watcher  │          │Collector │         │ Detector │
    │          │          │          │         │          │
    │ (Railway)│          │(Railway) │         │(Railway) │
    └──────────┘          └──────────┘         └──────────┘
         ▲                      ▲                    ▲
    Monitors              Collects CPU/MEM      Analyzes Data
    System Logs           Disk/Network           From API
```

## Option 1: Deploy to Railway.app (Recommended)

Railway.app offers:
- **Free tier**: 500 hours/month per project
- **Persistent storage**: Volumes for state
- **Background workers**: Perfect for agents
- **Environment variables**: Native support
- **Logging**: Built-in log viewing
- **GitHub integration**: Auto-deploy from git

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Start Free"
3. Sign up with GitHub (recommended) or email
4. Connect your GitHub account

### Step 2: Set Up Log Watcher Agent

1. **Create new project:**
   - Click "New Project"
   - Select "GitHub Repo"
   - Select your distributed-log-analytics repo
   - Give it a name (e.g., "log-watcher-prod")

2. **Configure:**
   - Railway auto-detects Python projects
   - It will use `requirements.txt` automatically
   - Set start command: `python agent/log_watcher_enhanced.py`

3. **Add environment variables:**
   ```
   API_URL=https://your-app.vercel.app
   LOG_FILE=/var/log/syslog
   POLL_INTERVAL=10
   BATCH_SIZE=100
   ```

4. **Deploy:**
   - Click "Deploy"
   - Monitor logs in Dashboard
   - Check status should show running (green)

### Step 3: Set Up Metrics Collector Agent

1. **Create new project:**
   - Click "New Project" → GitHub Repo
   - Same repo
   - Name: "metrics-collector-prod"

2. **Install psutil dependency:**
   - Update `requirements.txt`:
     ```
     fastapi==0.104.1
     uvicorn==0.24.0
     pydantic==2.5.0
     python-dotenv==1.0.0
     supabase==2.4.0
     psycopg2-binary==2.9.9
     aiohttp==3.9.1
     psutil==5.9.6
     ```

3. **Configure:**
   - Start command: `python agent/metrics_collector_enhanced.py`
   - Environment variables:
     ```
     API_URL=https://your-app.vercel.app
     POLL_INTERVAL=30
     ```

4. **Deploy:**
   - Click "Deploy"
   - Wait for installation (takes ~1-2 minutes)

### Step 4: Set Up Anomaly Detector Agent

1. **Create new project:**
   - Click "New Project" → GitHub Repo
   - Name: "anomaly-detector-prod"

2. **Configure:**
   - Start command: `python agent/anomaly_detector_enhanced.py`
   - Environment variables:
     ```
     API_URL=https://your-app.vercel.app
     POLL_INTERVAL=60
     ANOMALY_THRESHOLD=5
     ```

3. **Deploy:**
   - Click "Deploy"

### Monitoring Railway Deployments

1. **View logs:**
   - Click on project
   - "Deployments" tab
   - Click running deployment
   - "Logs" tab shows real-time output

2. **Check status:**
   - Green badge = Running
   - Yellow badge = Deploying
   - Red badge = Error

3. **Restart agent:**
   - Settings → Deployment → Restart

## Option 2: Deploy to Render.com

Render.com offers:
- **Free tier**: Always-on services
- **GitHub integration**: Auto-deploy
- **Web services**: For APIs
- **Background workers**: For agents
- **Custom domains**: Free SSL

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with GitHub or email
4. Connect GitHub repo

### Step 2: Create Log Watcher Service

1. **New → Background Worker**
2. **Configuration:**
   - **Name:** log-watcher-prod
   - **Repository:** your repo
   - **Branch:** main
   - **Runtime:** Python 3.9+
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python agent/log_watcher_enhanced.py`

3. **Environment Variables:**
   ```
   API_URL=https://your-app.vercel.app
   LOG_FILE=/var/log/syslog
   POLL_INTERVAL=10
   BATCH_SIZE=100
   ```

4. **Advanced:**
   - Auto-deploy: On
   - Keep alive: On (for paid plans)

5. **Create Service**

### Step 3: Create Metrics Collector Service

1. **New → Background Worker**
2. **Configuration:**
   - **Name:** metrics-collector-prod
   - **Start Command:** `python agent/metrics_collector_enhanced.py`

3. **Environment Variables:**
   ```
   API_URL=https://your-app.vercel.app
   POLL_INTERVAL=30
   ```

4. **Create Service**

### Step 4: Create Anomaly Detector Service

1. **New → Background Worker**
2. **Configuration:**
   - **Name:** anomaly-detector-prod
   - **Start Command:** `python agent/anomaly_detector_enhanced.py`

3. **Environment Variables:**
   ```
   API_URL=https://your-app.vercel.app
   POLL_INTERVAL=60
   ANOMALY_THRESHOLD=5
   ```

4. **Create Service**

## Option 3: Deploy to Fly.io (Docker)

Fly.io is best for containerized deployments.

### Step 1: Install Fly CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Create Docker Setup

Create `Dockerfile` in root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Can build image for any agent or use entrypoint override
ENV PYTHONUNBUFFERED=1

CMD ["python", "agent/log_watcher_enhanced.py"]
```

### Step 3: Create fly.toml

```toml
app = "log-analytics-watcher"
primary_region = "sfo"

[build]
  image = "log-watcher:latest"

[env]
  API_URL = "https://your-app.vercel.app"
  LOG_FILE = "/var/log/syslog"
  POLL_INTERVAL = "10"
```

### Step 4: Deploy

```bash
fly auth login
fly launch
fly deploy
```

## Monitoring and Logs

### Railway.app Logs

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs --project="log-watcher-prod"
```

### Render.com Logs

1. Dashboard → Service → Logs
2. View real-time output
3. Search logs by keyword

### Fly.io Logs

```bash
fly logs --app log-analytics-watcher
```

## Testing Agent Connectivity

### Test from Agent to API

Add this health check to each agent:

```python
async def test_api_connection():
    """Test if API is reachable"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/health") as resp:
                print(f"API Health: {resp.status}")
                data = await resp.json()
                print(f"Response: {data}")
        except Exception as e:
            print(f"Error: {e}")

# Run test
asyncio.run(test_api_connection())
```

### Test Log Ingestion

```bash
curl -X POST "https://your-app.vercel.app/logs/ingest" \
  -G --data-urlencode "message=Test log from agent" \
  -G --data-urlencode "level=INFO" \
  -G --data-urlencode "source=test-agent"
```

### Check Dashboard

1. Visit https://your-app.vercel.app
2. Verify logs/metrics/alerts appear
3. Check timestamps match agent execution time

## Troubleshooting

### Agent Not Starting

**Railway:**
1. Check Build Logs (different from Runtime Logs)
2. Verify Python version compatibility
3. Check all requirements are in `requirements.txt`

```bash
# Common error: Missing packages
pip freeze > requirements.txt
```

**Render:**
1. Check Build section for errors
2. Verify Start Command syntax
3. Build logs shown in Dashboard

### Agent Can't Reach API

**Common causes:**
1. Wrong `API_URL` (missing https://)
2. Vercel app URL incorrect
3. CORS not enabled on API
4. Network timeout (API too slow)

**Debug:**
```python
# Add to agent main()
print(f"API_URL: {API_URL}")
await self.check_health()  # Built-in health check
```

### High CPU/Memory Usage

**Log Watcher:**
- Increase `POLL_INTERVAL` (default: 10s)
- Decrease `BATCH_SIZE` (default: 100)
- Check log file size

**Metrics Collector:**
- Increase `POLL_INTERVAL` (default: 30s)
- psutil is lightweight, shouldn't be high

**Anomaly Detector:**
- Reduce history size (currently 100 metrics)
- Increase `POLL_INTERVAL` (default: 60s)

### Database Connection Errors

If using PostgreSQL:

1. Check `SUPABASE_URL` and `SUPABASE_KEY` are set in Vercel
2. Verify Supabase project is active
3. Check network access (some regions may need allowlisting)

## Auto-Scaling Configuration

### Railway.app

1. Project Settings → Auto Deploy
   - Auto Deploy: On (on main branch push)

2. Service Settings → Restart Policy
   - Always Restart: On
   - Max Restarts: 10

### Render.com

1. Service Settings → Auto Deploy
   - Auto Deploy: On

2. Free tier: Single instance only
   - Paid plans support scaling

### Fly.io

```bash
# Auto-scale based on CPU
fly scale memory 512 --app log-analytics-watcher
fly scale count 2 --app log-analytics-watcher
```

## Cost Estimation

### Monthly Cost (Production)

| Service | Tier | Monthly Cost | Notes |
|---------|------|-------------|-------|
| Railway | Free | $0 | 500 hours = 21 days continuous |
| Railway | Starter | $5 | Unlimited hours, $0.40/GB RAM |
| Render | Free | $0 | Always-on, limited resources |
| Render | Paid | $7-12 | Standard tier for reliability |
| Fly.io | Free | $0 | 3 shared VMs |
| Fly.io | Paid | $3-10 | Dedicated resources |
| Vercel | Free | $0 | 100 GB bandwidth |
| Supabase | Free | $0 | 500MB database |
| Supabase | Pro | $25 | 8GB database + backups |

**Recommended setup:**
- Vercel free (API): $0
- Railway starter (3 agents): $5
- Supabase free (database): $0
- **Total: $5/month**

## Production Checklist

- [ ] API deployed to Vercel
- [ ] Database created in Supabase
- [ ] Environment variables set in Vercel
- [ ] Log Watcher deployed to Railway
- [ ] Metrics Collector deployed to Railway
- [ ] Anomaly Detector deployed to Railway
- [ ] All agents can reach API (check logs)
- [ ] Logs appearing in dashboard
- [ ] Metrics being collected
- [ ] Alerts being generated
- [ ] Auto-deploy enabled
- [ ] Monitoring/alerting set up
- [ ] Error logs reviewed

## Next Steps

1. **Configure alerts:** Set up email/Slack notifications in your API
2. **Add authentication:** Implement JWT tokens for API security
3. **Scale agents:** Deploy additional agents for different log sources
4. **Custom dashboards:** Create role-based views
5. **Analytics:** Track metrics over time with historical data

## Support Resources

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Fly.io Docs: https://fly.io/docs
- FastAPI: https://fastapi.tiangolo.com
- Supabase: https://supabase.io/docs
