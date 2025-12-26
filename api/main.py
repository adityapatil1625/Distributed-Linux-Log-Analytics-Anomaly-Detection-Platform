"""
Vercel Serverless Function Handler for FastAPI
This file is the entry point for Vercel's serverless functions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
import os
from datetime import datetime
from typing import List

# Create FastAPI app
app = FastAPI(
    title="Distributed Log Analytics Platform",
    version="0.1.0",
    description="Serverless distributed log analytics on Vercel"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
logs_db = []
metrics_db = []
alerts_db = []

# ==================== LOGS ENDPOINTS ====================

@app.get("/api/logs/search")
async def search_logs(query: str = "", limit: int = 50, offset: int = 0):
    """Search logs"""
    return {
        "query": query,
        "limit": limit,
        "offset": offset,
        "results": logs_db[offset:offset+limit],
        "total": len(logs_db),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/logs/stats")
async def log_stats():
    """Get log statistics"""
    return {
        "total_logs": len(logs_db),
        "by_level": {
            "ERROR": 0,
            "WARN": 0,
            "INFO": 0,
            "DEBUG": 0
        }
    }

@app.post("/api/logs/ingest")
async def ingest_log(log_entry: dict):
    """Ingest a log entry"""
    log_entry["timestamp"] = datetime.now().isoformat()
    logs_db.append(log_entry)
    return {"status": "success", "id": len(logs_db)}

# ==================== METRICS ENDPOINTS ====================

@app.get("/api/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "cpu_usage": 0,
        "memory_usage": 0,
        "disk_usage": 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/metrics/history")
async def metrics_history(hours: int = 24):
    """Get metrics history"""
    return {
        "hours": hours,
        "data": metrics_db[-100:],
        "total": len(metrics_db)
    }

@app.post("/api/metrics/record")
async def record_metric(metric: dict):
    """Record a metric"""
    metric["timestamp"] = datetime.now().isoformat()
    metrics_db.append(metric)
    return {"status": "success"}

# ==================== ALERTS ENDPOINTS ====================

@app.get("/api/alerts")
async def get_alerts(severity: str = None):
    """Get alerts"""
    filtered = alerts_db
    if severity:
        filtered = [a for a in alerts_db if a.get("severity") == severity]
    
    return {
        "alerts": filtered,
        "critical": len([a for a in alerts_db if a.get("severity") == "CRITICAL"]),
        "warning": len([a for a in alerts_db if a.get("severity") == "WARNING"]),
        "info": len([a for a in alerts_db if a.get("severity") == "INFO"]),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/alerts")
async def create_alert(alert: dict):
    """Create an alert"""
    alert["id"] = len(alerts_db) + 1
    alert["timestamp"] = datetime.now().isoformat()
    alerts_db.append(alert)
    return {"status": "success", "alert_id": alert["id"]}

@app.delete("/api/alerts/{alert_id}")
async def dismiss_alert(alert_id: int):
    """Dismiss an alert"""
    global alerts_db
    alerts_db = [a for a in alerts_db if a.get("id") != alert_id]
    return {"status": "success", "dismissed_id": alert_id}

# ==================== UTILITY ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Distributed Log Analytics Platform API",
        "status": "healthy",
        "version": "0.1.0",
        "deployment": "vercel",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "log-analytics",
        "environment": os.getenv("VERCEL_ENV", "development")
    }

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Distributed Log Analytics Platform",
        "version": "0.1.0",
        "environment": os.getenv("VERCEL_ENV", "development"),
        "docs": "/api/docs",
        "openapi": "/api/openapi.json",
        "endpoints": {
            "logs": {
                "search": "GET /api/logs/search",
                "stats": "GET /api/logs/stats",
                "ingest": "POST /api/logs/ingest"
            },
            "metrics": {
                "current": "GET /api/metrics",
                "history": "GET /api/metrics/history",
                "record": "POST /api/metrics/record"
            },
            "alerts": {
                "list": "GET /api/alerts",
                "create": "POST /api/alerts",
                "dismiss": "DELETE /api/alerts/{id}"
            }
        }
    }

# Export the app for Vercel
__all__ = ["app"]
