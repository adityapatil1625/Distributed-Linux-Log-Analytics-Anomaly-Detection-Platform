from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import List, Optional

router = APIRouter()

# Mock database
logs_db = []

@router.get("/search")
async def search_logs(
    query: str = Query("", description="Search query"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Search logs with pagination
    """
    return {
        "query": query,
        "limit": limit,
        "offset": offset,
        "results": logs_db[offset:offset+limit],
        "total": len(logs_db),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/stats")
async def log_stats():
    """
    Get log statistics
    """
    return {
        "total_logs": len(logs_db),
        "last_24h": len([l for l in logs_db if True]),  # Placeholder
        "by_level": {
            "ERROR": 0,
            "WARN": 0,
            "INFO": 0,
            "DEBUG": 0
        }
    }

@router.post("/ingest")
async def ingest_log(log_entry: dict):
    """
    Ingest a single log entry (simplified for Vercel)
    Note: For high-volume ingestion, use separate ingestion service
    """
    log_entry["timestamp"] = datetime.now().isoformat()
    logs_db.append(log_entry)
    return {"status": "success", "id": len(logs_db)}
