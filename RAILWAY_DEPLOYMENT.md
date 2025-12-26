# 🚀 Deploy Agents to Railway.app

Railway is perfect for deploying the distributed agents (log watchers, collectors, TCP server).

## ✨ Why Railway for Agents?

- ✅ Persistent background processes
- ✅ Easy deployment from GitHub
- ✅ Environmental variables support
- ✅ PostgreSQL included
- ✅ Affordable ($5/month per service)
- ✅ No cold starts

## 📋 Quick Setup

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign in with GitHub
3. Create new project

### Step 2: Deploy Log Watcher (Highest Priority)

Create `railway.yml` in root:
```yaml
build:
  builder: nixpacks

deploy:
  startCommand: python agent/log_watcher.py
```

Then:
```bash
npm install -g @railway/cli
railway login
railway link
railway up
```

### Step 3: Deploy Collector Service

```yaml
build:
  builder: nixpacks

deploy:
  startCommand: python agent/collector.py
```

### Step 4: Deploy TCP Server

```yaml
build:
  builder: nixpacks

deploy:
  startCommand: python ingestion/tcp_server.py
```

## 🔗 Connect to Vercel API

Add environment variable to each Railway service:

```
API_URL=https://your-app.vercel.app
```

Agents will send logs to: `https://your-app.vercel.app/logs/ingest`

## 📊 File Structure for Railway

```
agent/
├── log_watcher.py      ← Monitors system logs
├── collector.py        ← Collects metrics
├── tcp_client.py       ← Sends data
├── proc_reader.py      ← Reads processes
└── requirements.txt

ingestion/
├── tcp_server.py       ← TCP listener
└── requirements.txt
```

## 🔧 Agent Implementation Example

### Log Watcher (Updated for API ingestion)

```python
import asyncio
import aiohttp
import os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")

async def watch_logs():
    """Watch system logs and send to API"""
    async with aiohttp.ClientSession() as session:
        # Example: Read system logs
        try:
            with open("/var/log/syslog", "r") as f:
                for line in f:
                    # Send to API
                    async with session.post(
                        f"{API_URL}/logs/ingest",
                        params={
                            "message": line.strip(),
                            "level": "INFO",
                            "source": "system"
                        }
                    ) as resp:
                        print(f"Log sent: {resp.status}")
                        
        except Exception as e:
            print(f"Error: {e}")
            await send_alert(session, "Log Watcher Error", str(e), "ERROR")

async def send_alert(session, title, message, severity):
    """Send alert to API"""
    async with session.post(
        f"{API_URL}/alerts",
        params={
            "title": title,
            "message": message,
            "severity": severity
        }
    ) as resp:
        print(f"Alert sent: {resp.status}")

async def main():
    while True:
        await watch_logs()
        await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    asyncio.run(main())
```

## 📡 TCP Server (Updated for API)

```python
import asyncio
import aiohttp
import os
import json

API_URL = os.getenv("API_URL", "http://localhost:8000")

async def handle_client(reader, writer):
    """Handle incoming TCP connections"""
    client_addr = writer.get_extra_info('peername')
    print(f"Client connected: {client_addr}")
    
    async with aiohttp.ClientSession() as session:
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                # Parse incoming log data
                message = data.decode().strip()
                
                # Send to API
                async with session.post(
                    f"{API_URL}/logs/ingest",
                    params={
                        "message": message,
                        "level": "INFO",
                        "source": "tcp_server"
                    }
                ) as resp:
                    writer.write(f"Log received: {resp.status}\n".encode())
                    await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

async def start_server():
    """Start TCP server"""
    server = await asyncio.start_server(
        handle_client,
        "0.0.0.0",
        5000
    )
    
    async with server:
        print("TCP Server listening on port 5000")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
```

## 🔐 Environment Variables on Railway

Set these in Railway dashboard:
```
API_URL=https://your-app.vercel.app
LOG_LEVEL=INFO
ENABLE_ANOMALY=true
DATABASE_URL=postgresql://...  (if using Railway database)
```

## 📊 Monitoring

Railway dashboard shows:
- Live logs from agents
- CPU/Memory usage
- Deployment history
- Error tracking

## 💡 Best Practices

1. **One service per agent** - Easier to manage and scale
2. **Set resource limits** - Railway charges per resource usage
3. **Use environment variables** - Never hardcode secrets
4. **Enable health checks** - Auto-restart on failure
5. **Monitor logs** - Check Railway dashboard regularly

## 🚨 Troubleshooting

### Agents can't reach Vercel API
```bash
# Check API is accessible
curl https://your-app.vercel.app/health
```

### TCP Server won't start
- Check port 5000 is available
- Verify environment variables set
- Check logs in Railway dashboard

### Out of memory
- Reduce polling frequency
- Lower batch sizes
- Add memory limit in Railway

## 📖 Resources

- Railway Docs: https://docs.railway.app
- Railway CLI: https://docs.railway.app/cli/quick-start
- Python Logging: https://docs.python.org/3/library/logging.html

## 🎯 Summary

```bash
# Deploy agents to Railway
railway up agent/log_watcher.py
railway up agent/collector.py
railway up ingestion/tcp_server.py

# Agents automatically send data to Vercel API
# API stores and displays on dashboard
# Everything syncs automatically!
```

---

**Agents deployed on Railway, API on Vercel = Complete distributed system!** 🚀
