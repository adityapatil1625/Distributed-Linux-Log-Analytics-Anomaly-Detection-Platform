from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Mock metrics storage
metrics_db = []

@router.get("/")
async def get_metrics():
    """
    Get system metrics
    """
    return {
        "cpu_usage": 0,
        "memory_usage": 0,
        "disk_usage": 0,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/history")
async def metrics_history(hours: int = 24):
    """
    Get metrics history
    """
    return {
        "hours": hours,
        "data": metrics_db[-100:],
        "total": len(metrics_db)
    }

@router.post("/record")
async def record_metric(metric: dict):
    """
    Record a new metric
    """
    metric["timestamp"] = datetime.now().isoformat()
    metrics_db.append(metric)
    return {"status": "success"}
