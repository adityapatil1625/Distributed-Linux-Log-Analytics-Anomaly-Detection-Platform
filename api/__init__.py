from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime

# Import routers
from .logs import router as logs_router
from .metrics import router as metrics_router
from .alerts import router as alerts_router

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

# Include routers
app.include_router(logs_router, prefix="/logs", tags=["logs"])
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Distributed Log Analytics Platform API",
        "status": "healthy",
        "version": "0.1.0",
        "deployment": "vercel",
        "timestamp": datetime.now().isoformat()
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "log-analytics",
        "environment": os.getenv("VERCEL_ENV", "development")
    }

# API info
@app.get("/api/info")
async def api_info():
    return {
        "name": "Distributed Log Analytics Platform",
        "version": "0.1.0",
        "environment": os.getenv("VERCEL_ENV", "development"),
        "docs": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "logs": "/logs/search",
            "metrics": "/metrics",
            "alerts": "/alerts",
            "health": "/health"
        }
    }
