# Distributed Log Analytics Platform

A production-ready distributed system for collecting, analyzing, and visualizing logs and metrics from multiple sources.

## ⚡ Quick Start (5 Minutes)

### 1. Deploy API to Vercel (2 min)

```bash
# Clone and deploy
git clone <your-repo-url>
cd distributed-log-analytics
vercel  # Follow prompts, auto-detects FastAPI
```

✅ API now running at `https://your-app.vercel.app`

### 2. Set Up PostgreSQL Database (2 min)

```bash
# Create free Supabase project
# 1. Go to supabase.com → New Project
# 2. Create database (takes ~30 seconds)
# 3. Copy URL and Key
# 4. Add to Vercel:
#    - Project Settings → Environment Variables
#    - SUPABASE_URL: paste URL
#    - SUPABASE_KEY: paste Key
# 5. Redeploy: vercel --prod
```

✅ Database connected, data persists

### 3. Deploy Agents (1 min)

```bash
# Railway.app (recommended for free tier)
# 1. Go to railway.app → New Project → GitHub Repo
# 2. Select your repo
# 3. Set start command: python agent/log_watcher_enhanced.py
# 4. Add environment: API_URL=https://your-app.vercel.app
# 5. Deploy

# Repeat for:
#   - metrics_collector_enhanced.py
#   - anomaly_detector_enhanced.py
```

✅ Agents sending data, dashboard shows live metrics

## 📊 Features

### Real-Time Dashboard
- Live log stream with search/filter
- System metrics (CPU, memory, disk)
- Alert management with severity levels
- Auto-refresh every 5 seconds
- Mobile responsive

### Distributed Agents
- **Log Watcher:** Monitors system logs, sends to API
- **Metrics Collector:** Tracks CPU/memory/disk/network
- **Anomaly Detector:** Analyzes patterns, generates alerts

### Production Ready
- ✅ PostgreSQL database (Supabase)
- ✅ Error handling & fallbacks
- ✅ Async operations for performance
- ✅ CORS enabled for any frontend
- ✅ Docker support for local development
- ✅ Environment variable configuration

## 🏗️ Architecture

```
User Dashboard (Web)
        ↓
   Vercel API (FastAPI)
   ├─ /logs/ingest (receive logs)
   ├─ /logs (search/filter)
   ├─ /metrics (record & retrieve)
   ├─ /alerts (manage)
   └─ /health (status)
        ↓
   Supabase (PostgreSQL)
        ↑
Distributed Agents (Railway)
├─ Log Watcher (send logs)
├─ Metrics Collector (send metrics)
└─ Anomaly Detector (analyze & alert)
```

## 📦 Project Structure

```
.
├── api/
│   ├── main.py              # FastAPI app + dashboard HTML
│   ├── database.py          # PostgreSQL abstraction layer
│   ├── logs.py              # Log endpoints
│   ├── metrics.py           # Metrics endpoints
│   └── alerts.py            # Alert endpoints
├── agent/
│   ├── log_watcher_enhanced.py       # Monitor system logs
│   ├── metrics_collector_enhanced.py  # Collect system metrics
│   └── anomaly_detector_enhanced.py   # Analyze & alert
├── dashboard/
│   └── webapp/
│       ├── app.txt          # Dashboard configuration
│       └── index.html       # Dashboard UI
├── Dockerfile               # Agent container image
├── Dockerfile.api          # API container image
├── docker-compose.yml      # Local dev environment
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
└── README.md              # This file
```

## 🚀 Deployment Options

### Option 1: Vercel + Railway (Recommended)
- **Cost:** $0-5/month
- **Ease:** ⭐⭐⭐⭐⭐
- **Performance:** Excellent

**Benefits:**
- Vercel: Auto-scaling, zero-config HTTPS, GitHub integration
- Railway: Always-on, persistent storage, environment variables
- PostgreSQL: Free tier with 500MB storage

### Option 2: Render.com
- **Cost:** $0-12/month  
- **Ease:** ⭐⭐⭐⭐
- **Performance:** Good

**Benefits:**
- All in one platform
- Auto-deploy from GitHub
- Free tier available

### Option 3: Fly.io (Docker)
- **Cost:** $0-10/month
- **Ease:** ⭐⭐⭐
- **Performance:** Excellent

**Benefits:**
- Container-native
- Global deployment
- Dedicated resources available

### Option 4: Local Development
```bash
# Start entire stack locally
docker-compose up

# API: http://localhost:8000
# Agents: Connected and running
# Database: Local SQLite (modify in code)
```

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
API_URL=https://your-app.vercel.app
DEBUG=false

# Database (Optional - defaults to in-memory if not set)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyxxxx...

# Agent Configuration
LOG_FILE=/var/log/syslog           # Log watcher
POLL_INTERVAL=30                   # Check interval (seconds)
BATCH_SIZE=100                     # Batch logs (log watcher)
ANOMALY_THRESHOLD=5                # Error threshold for alerts
```

### Create `.env` File

```bash
cp .env.example .env
# Edit .env with your values
```

## 📝 API Endpoints

### Logs
```bash
# Ingest log
POST /logs/ingest?message=...&level=INFO&source=myapp

# Get logs
GET /logs?limit=100&level=ERROR

# Search logs
GET /logs/search?query=error

# Log statistics
GET /logs/stats
```

### Metrics
```bash
# Record metric
POST /metrics?name=cpu_usage&value=45&unit=%&source=server1

# Get metrics
GET /metrics?limit=100&name=cpu_usage

# Get metrics history
GET /metrics/history?name=memory_usage&hours=24
```

### Alerts
```bash
# Create alert
POST /alerts?title=...&message=...&severity=CRITICAL

# Get alerts
GET /alerts?severity=ERROR&limit=50

# Resolve alert
PUT /alerts/{id}/resolve
```

### System
```bash
# Health check
GET /health

# API info
GET /info

# Dashboard
GET /
```

## 🧪 Testing

### Test API Endpoints

```bash
# Send a test log
curl -X POST "https://your-app.vercel.app/logs/ingest" \
  -G --data-urlencode "message=Test log" \
  -G --data-urlencode "level=INFO" \
  -G --data-urlencode "source=curl"

# Get recent logs
curl "https://your-app.vercel.app/logs?limit=10"

# Send a metric
curl -X POST "https://your-app.vercel.app/metrics" \
  -G --data-urlencode "name=test_metric" \
  -G --data-urlencode "value=42"

# Get metrics
curl "https://your-app.vercel.app/metrics?limit=10"
```

### Test Local Setup

```bash
# Start stack
docker-compose up

# In another terminal, send test log
curl -X POST "http://localhost:8000/logs/ingest" \
  -G --data-urlencode "message=Test" \
  -G --data-urlencode "level=INFO"

# View dashboard
open http://localhost:8000
```

## 📚 Documentation

- [Agent Deployment Guide](./AGENT_DEPLOYMENT.md) - Deploy to Railway, Render, Fly.io
- [Database Setup](./SUPABASE_SETUP.md) - PostgreSQL with Supabase
- [API Documentation](./api/main.py) - Endpoint specifications
- [Dashboard Features](./dashboard/webapp/app.txt) - UI functionality

## 🐛 Troubleshooting

### Dashboard shows "Disconnected"

1. Check API_URL in browser console
2. Verify Vercel deployment is active
3. Check CORS headers: `Access-Control-Allow-Origin: *`

### Agents not sending data

1. Verify API_URL is correct in environment variables
2. Check agent logs: `railway logs`
3. Test connectivity: `curl https://your-app.vercel.app/health`

### Database not persisting data

1. Verify SUPABASE_URL and SUPABASE_KEY are set
2. Check Supabase project is active
3. Review database schema in Supabase console
4. Check Vercel logs for database errors

### High CPU/Memory usage

**Log Watcher:**
- Increase `POLL_INTERVAL` (less frequent checks)
- Decrease `BATCH_SIZE` (process logs in smaller batches)

**Metrics Collector:**
- Increase `POLL_INTERVAL` (default 30s is good)

**Anomaly Detector:**
- Increase `POLL_INTERVAL` (default 60s is good)

## 🔐 Security

### Recommended

- [ ] Add API authentication (JWT tokens)
- [ ] Enable HTTPS everywhere (Vercel handles this)
- [ ] Use environment variables for secrets
- [ ] Enable Row-Level Security in Supabase
- [ ] Rate limit API endpoints
- [ ] Add user authentication to dashboard

### Implemented

- ✅ CORS enabled
- ✅ Error handling (no stack traces exposed)
- ✅ Environment-based configuration
- ✅ Supabase connection pooling

## 📈 Scaling

### For 1M+ logs/day

1. **Database:** Upgrade Supabase to Pro tier ($25/month)
2. **API:** Add caching layer (Redis)
3. **Agents:** Deploy multiple instances per source
4. **Analytics:** Add retention policy (delete logs >30 days)

### Cost Estimation

| Component | Free | Pro | Notes |
|-----------|------|-----|-------|
| Vercel API | $0 | $20/month | Bandwidth overage |
| Railway Agents | $0 | $5+/month | 3 agents starter |
| Supabase DB | $0 | $25/month | 8GB storage |
| **Total** | **$0** | **$50/month** | Production-ready |

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and create PR

## 📄 License

MIT - See LICENSE file

## 🆘 Support

- GitHub Issues: [Report bugs](../../issues)
- Documentation: See `./docs/` folder
- Discord: [Join community](https://discord.gg/...)

## 🎯 Roadmap

- [ ] User authentication with JWT
- [ ] Custom alerting rules engine
- [ ] Advanced analytics & ML anomaly detection
- [ ] Mobile app (iOS/Android)
- [ ] Slack/PagerDuty integration
- [ ] Grafana dashboard integration
- [ ] Log retention policies
- [ ] Multi-tenant support
- [ ] Dark theme for dashboard
- [ ] Log streaming (WebSocket)

## 📞 Quick Links

- **API Docs:** https://your-app.vercel.app/docs
- **Dashboard:** https://your-app.vercel.app
- **Supabase Console:** https://app.supabase.com
- **Railway Dashboard:** https://railway.app
- **Vercel Dashboard:** https://vercel.com/dashboard

---

**Made with ❤️ by the Log Analytics Team**
