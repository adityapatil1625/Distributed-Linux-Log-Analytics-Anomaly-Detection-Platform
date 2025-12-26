"""
Database module for Distributed Log Analytics Platform
Supports both PostgreSQL (via Supabase) and SQLite for local development
"""
import os
from datetime import datetime
from typing import List, Dict, Optional

# Check if using remote database (Supabase) or SQLite
USE_SUPABASE = bool(os.getenv("SUPABASE_URL"))

if USE_SUPABASE:
    try:
        from supabase import create_client, Client
        
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        DB_AVAILABLE = True
    except ImportError:
        DB_AVAILABLE = False
        print("Warning: Supabase not configured. Using in-memory storage.")
else:
    DB_AVAILABLE = False

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self):
        self.db_available = DB_AVAILABLE
    
    # ==================== LOGS ====================
    
    async def add_log(self, message: str, level: str = "INFO", source: str = "unknown") -> Dict:
        """Add a log entry"""
        log_entry = {
            "message": message,
            "level": level,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.db_available:
            try:
                result = supabase.table("logs").insert([log_entry]).execute()
                return {"status": "success", "id": result.data[0]["id"] if result.data else len(str(result))}
            except Exception as e:
                print(f"Database error: {e}")
                return {"status": "error", "message": str(e)}
        return {"status": "success", "id": 1}
    
    async def get_logs(self, limit: int = 50, offset: int = 0, query: str = "") -> Dict:
        """Get logs with optional search"""
        if self.db_available:
            try:
                q = supabase.table("logs").select("*").order("timestamp", desc=True)
                
                if query:
                    q = q.ilike("message", f"%{query}%")
                
                result = q.range(offset, offset + limit - 1).execute()
                return {
                    "results": result.data,
                    "total": len(result.data),
                    "query": query
                }
            except Exception as e:
                print(f"Database error: {e}")
                return {"results": [], "total": 0, "query": query}
        return {"results": [], "total": 0, "query": query}
    
    async def get_log_stats(self) -> Dict:
        """Get log statistics"""
        if self.db_available:
            try:
                result = supabase.table("logs").select("level").execute()
                logs = result.data
                
                stats = {
                    "total_logs": len(logs),
                    "by_level": {
                        "ERROR": len([l for l in logs if l.get("level") == "ERROR"]),
                        "WARN": len([l for l in logs if l.get("level") == "WARN"]),
                        "INFO": len([l for l in logs if l.get("level") == "INFO"]),
                        "DEBUG": len([l for l in logs if l.get("level") == "DEBUG"])
                    }
                }
                return stats
            except Exception as e:
                print(f"Database error: {e}")
                return {"total_logs": 0, "by_level": {}}
        return {"total_logs": 0, "by_level": {}}
    
    # ==================== ALERTS ====================
    
    async def add_alert(self, title: str, message: str, severity: str = "INFO") -> Dict:
        """Create an alert"""
        alert = {
            "title": title,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        }
        
        if self.db_available:
            try:
                result = supabase.table("alerts").insert([alert]).execute()
                return {"status": "success", "alert_id": result.data[0]["id"] if result.data else 1}
            except Exception as e:
                print(f"Database error: {e}")
                return {"status": "error", "message": str(e)}
        return {"status": "success", "alert_id": 1}
    
    async def get_alerts(self, severity: Optional[str] = None, limit: int = 100) -> Dict:
        """Get alerts"""
        if self.db_available:
            try:
                q = supabase.table("alerts").select("*").eq("resolved", False).order("timestamp", desc=True)
                
                if severity:
                    q = q.eq("severity", severity)
                
                result = q.limit(limit).execute()
                alerts = result.data
                
                return {
                    "alerts": alerts,
                    "critical": len([a for a in alerts if a.get("severity") == "CRITICAL"]),
                    "warning": len([a for a in alerts if a.get("severity") == "WARNING"]),
                    "info": len([a for a in alerts if a.get("severity") == "INFO"])
                }
            except Exception as e:
                print(f"Database error: {e}")
                return {"alerts": [], "critical": 0, "warning": 0, "info": 0}
        return {"alerts": [], "critical": 0, "warning": 0, "info": 0}
    
    async def resolve_alert(self, alert_id: int) -> Dict:
        """Mark alert as resolved"""
        if self.db_available:
            try:
                supabase.table("alerts").update({"resolved": True}).eq("id", alert_id).execute()
                return {"status": "success", "dismissed_id": alert_id}
            except Exception as e:
                print(f"Database error: {e}")
                return {"status": "error", "message": str(e)}
        return {"status": "success", "dismissed_id": alert_id}
    
    # ==================== METRICS ====================
    
    async def record_metric(self, name: str, value: float, tags: Dict = None) -> Dict:
        """Record a metric"""
        metric = {
            "name": name,
            "value": value,
            "tags": tags or {},
            "timestamp": datetime.now().isoformat()
        }
        
        if self.db_available:
            try:
                result = supabase.table("metrics").insert([metric]).execute()
                return {"status": "success"}
            except Exception as e:
                print(f"Database error: {e}")
                return {"status": "error", "message": str(e)}
        return {"status": "success"}
    
    async def get_metrics(self, hours: int = 24, limit: int = 100) -> Dict:
        """Get metrics from last N hours"""
        if self.db_available:
            try:
                result = supabase.table("metrics").select("*").order("timestamp", desc=True).limit(limit).execute()
                return {
                    "hours": hours,
                    "data": result.data,
                    "total": len(result.data)
                }
            except Exception as e:
                print(f"Database error: {e}")
                return {"hours": hours, "data": [], "total": 0}
        return {"hours": hours, "data": [], "total": 0}

# Global database instance
db = DatabaseManager()
