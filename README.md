# Distributed Linux Log Analytics & Anomaly Detection Platform
A comprehensive log analytics and anomaly detection system with distributed agents, real-time log ingestion, and Vercel serverless deployment.

## 🚀 Quick Start

### Deploy to Vercel

**Option 1: Using Vercel CLI**
```bash
npm install -g vercel
vercel
```

**Option 2: Using GitHub**
1. Push to GitHub
2. Visit https://vercel.com/new
3. Import your repository
4. Deploy!

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
uvicorn api.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

## 📋 Project Structure

```
api/                          # Vercel serverless API (FastAPI)
├── main.py                   # Main application with all endpoints
├── index.py                  # Root handler
├── logs.py                   # Log search & ingestion endpoints
├── metrics.py                # Metrics endpoints
└── alerts.py                 # Alert management endpoints

backend/                       # Original backend (see VERCEL_DEPLOYMENT.md)
agent/                         # Distributed log collectors
anomaly/                       # Anomaly detection engine
ingestion/                     # TCP-based log ingestion
dashboard/                     # Frontend (placeholder)
index/                         # Log indexing system
```

## 🌐 API Endpoints

### Logs
- `GET /api/logs/search?query=...` - Search logs
- `GET /api/logs/stats` - Log statistics
- `POST /api/logs/ingest` - Ingest a log entry

### Metrics
- `GET /api/metrics` - Current metrics
- `GET /api/metrics/history?hours=24` - Historical metrics
- `POST /api/metrics/record` - Record a metric

### Alerts
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create an alert
- `DELETE /api/alerts/{id}` - Dismiss an alert

### Health & Info
- `GET /` - Root status
- `GET /health` - Health check
- `GET /api/info` - API information

## 📚 Documentation

- **Swagger UI**: `/docs` (interactive API explorer)
- **ReDoc**: `/redoc` (API reference)
- **OpenAPI**: `/openapi.json`
- **Deployment Guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

## 🔧 Configuration

Set environment variables in Vercel dashboard:

```env
LOG_RETENTION_DAYS=30
MAX_LOG_SIZE_MB=100
ENABLE_ANOMALY_DETECTION=true
API_TIMEOUT_SECONDS=30
```

For local development, copy `.env.example` to `.env.local`:
```bash
cp .env.example .env.local
```

## ⚙️ Deployment Options

| Platform | Best For | Setup Time |
|----------|----------|-----------|
| **Vercel** | FastAPI HTTP API | 2 minutes |
| **Railway** | Full distributed system | 5 minutes |
| **Render** | Python apps with workers | 5 minutes |
| **AWS EC2** | Full control & scaling | 15 minutes |

### Component Deployment Matrix

| Component | Vercel | Railway | Render | AWS |
|-----------|--------|---------|--------|-----|
| FastAPI API | ✅ | ✅ | ✅ | ✅ |
| Log Agents | ❌ | ✅ | ✅ | ✅ |
| TCP Server | ❌ | ✅ | ✅ | ✅ |
| Database | ❌ | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ✅ | ✅ |

## 🔍 Testing

```bash
# Test API locally
curl http://localhost:8000/health
curl http://localhost:8000/api/info
curl "http://localhost:8000/api/logs/search?query=error"
```

## 📝 Important Notes

### Vercel Limitations
- **Stateless execution**: Use external database for persistence
- **Timeout limit**: 10-60 seconds depending on plan
- **Memory limit**: 512MB
- **No persistent storage**: Data lost between deployments

### Current Implementation
The API uses in-memory storage. For production:
- Add PostgreSQL/MongoDB
- Implement caching (Redis)
- Add authentication
- Set up proper error handling

### Distributed Components
- **Agents** & **TCP Server** need separate hosting
- See deployment guide for options

## 📖 Learn More

- [Vercel Deployment Guide](VERCEL_DEPLOYMENT.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vercel Python Support](https://vercel.com/docs/serverless-functions/python)

## 📜 License

MIT License