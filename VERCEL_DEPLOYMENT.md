# Vercel Deployment Guide

## Project Structure for Vercel

Your project has been restructured for Vercel serverless deployment:

```
api/
├── main.py          # Main FastAPI app with all endpoints
├── index.py         # Root handler
├── logs.py          # Logs router
├── metrics.py       # Metrics router
├── alerts.py        # Alerts router
└── __init__.py      # Package initialization

vercel.json          # Vercel configuration
requirements.txt     # Python dependencies
.env.example         # Environment variables template
```

## Prerequisites

1. **Vercel Account**: https://vercel.com
2. **Git**: Repository initialized
3. **Node.js**: For Vercel CLI (optional but recommended)

## Installation & Setup

### Option 1: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd c:\Users\adity\Downloads\distributed-log-analytics
vercel
```

### Option 2: Deploy via GitHub

1. Push this repository to GitHub
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel will auto-detect the configuration
5. Click Deploy

## Configuration

### Environment Variables

Set these in Vercel dashboard (Settings → Environment Variables):

```
LOG_RETENTION_DAYS=30
MAX_LOG_SIZE_MB=100
ENABLE_ANOMALY_DETECTION=true
API_TIMEOUT_SECONDS=30
```

Or use `.env.local` for local development:
```bash
cp .env.example .env.local
```

## API Endpoints

After deployment, your API will be available at: `https://your-project.vercel.app`

### Logs
- `GET /api/logs/search?query=...` - Search logs
- `GET /api/logs/stats` - Get log statistics
- `POST /api/logs/ingest` - Ingest a log entry

### Metrics
- `GET /api/metrics` - Get current metrics
- `GET /api/metrics/history?hours=24` - Get metrics history
- `POST /api/metrics/record` - Record a new metric

### Alerts
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create an alert
- `DELETE /api/alerts/{id}` - Dismiss an alert

### Utilities
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/info` - API information

## Documentation

Interactive API docs available at:
- Swagger UI: `https://your-project.vercel.app/docs`
- ReDoc: `https://your-project.vercel.app/redoc`
- OpenAPI JSON: `https://your-project.vercel.app/openapi.json`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.main:app --reload

# Visit http://localhost:8000
```

## Important Notes

### Vercel Limitations

1. **Stateless**: Each function execution is independent. Use external database for persistence
2. **Cold starts**: First request may be slower
3. **Execution timeout**: 10 seconds (Hobby) to 60 seconds (Pro)
4. **Memory limit**: 512MB
5. **No persistent storage**: Use external databases

### Current Implementation

The current implementation uses in-memory storage (lists) which **will not persist between deployments**. For production:

- Use PostgreSQL, MongoDB, or similar
- Implement caching (Redis)
- Add authentication
- Set up proper error handling

### Agent/Ingestion Services

The distributed nature of your project means:

- **Agents** (log watchers, collectors) should run on separate infrastructure
- **TCP server** should run on a dedicated server (VPS, EC2)
- **Vercel** handles the HTTP API only

For a complete distributed solution, deploy these components to:
- Railway.app
- Render.com
- AWS EC2 / Lambda
- DigitalOcean

## Deployment Status

- [x] API restructured for Vercel
- [x] Requirements.txt created
- [x] vercel.json configured
- [x] Environment variables setup
- [x] CORS enabled
- [x] Health checks added

## Next Steps

1. Set environment variables in Vercel dashboard
2. Deploy via `vercel` CLI or GitHub
3. Test endpoints with curl or Postman
4. Add database integration (PostgreSQL/MongoDB)
5. Deploy agents to separate services
6. Set up CI/CD pipeline

## Troubleshooting

### Build fails with module errors
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility

### 502 Bad Gateway
- Check logs in Vercel dashboard
- Ensure API endpoints are correctly configured
- Test locally with `uvicorn api.main:app --reload`

### Cold start too slow
- This is normal on Vercel's free tier
- Upgrade to Pro for faster cold starts

## Support

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Vercel Python Support: https://vercel.com/docs/serverless-functions/python
