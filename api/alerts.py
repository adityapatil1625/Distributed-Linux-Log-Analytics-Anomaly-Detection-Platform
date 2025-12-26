from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Mock alerts storage
alerts_db = []

@router.get("/")
async def get_alerts(severity: str = None):
    """
    Get alerts, optionally filtered by severity
    """
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

@router.post("/")
async def create_alert(alert: dict):
    """
    Create a new alert
    """
    alert["id"] = len(alerts_db) + 1
    alert["timestamp"] = datetime.now().isoformat()
    alerts_db.append(alert)
    return {"status": "success", "alert_id": alert["id"]}

@router.delete("/{alert_id}")
async def dismiss_alert(alert_id: int):
    """
    Dismiss an alert
    """
    global alerts_db
    alerts_db = [a for a in alerts_db if a.get("id") != alert_id]
    return {"status": "success", "dismissed_id": alert_id}
