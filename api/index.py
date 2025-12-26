from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Distributed Log Analytics Platform",
    version="0.1.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Root ----------
@app.get("/")
def root():
    return {"message": "Distributed Log Analytics Platform API is running 🚀", "status": "healthy"}

# ---------- Health Check ----------
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "log-analytics"}

# ---------- Metrics ----------
@app.get("/metrics")
def get_metrics():
    return {
        "status": "ok", 
        "data": {
            "total_logs": 0,
            "anomalies_detected": 0,
            "uptime": "100%"
        }
    }

# ---------- Log search ----------
@app.get("/logs/search")
def search_logs(query: str = ""):
    return {
        "query": query, 
        "results": [],
        "total": 0,
        "timestamp": "2025-12-25T00:00:00Z"
    }

# ---------- Alerts ----------
@app.get("/alerts")
def get_alerts():
    return {
        "alerts": [],
        "critical": 0,
        "warning": 0,
        "info": 0
    }

# ---------- API Info ----------
@app.get("/api/info")
def api_info():
    return {
        "name": "Distributed Log Analytics Platform",
        "version": "0.1.0",
        "environment": "production",
        "endpoints": [
            "/",
            "/health",
            "/metrics",
            "/logs/search",
            "/alerts",
            "/api/info"
        ]
    }
