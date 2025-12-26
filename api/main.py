"""
Vercel Serverless Function Handler for FastAPI
This file is the entry point for Vercel's serverless functions
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
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
logs_db = [
    {"message": "Application started successfully", "level": "INFO", "timestamp": datetime.now().isoformat()},
    {"message": "Database connection established", "level": "INFO", "timestamp": datetime.now().isoformat()},
    {"message": "Cache initialized with 1000 entries", "level": "INFO", "timestamp": datetime.now().isoformat()},
    {"message": "Warning: High memory usage detected", "level": "WARN", "timestamp": datetime.now().isoformat()},
    {"message": "Error: Connection timeout to external service", "level": "ERROR", "timestamp": datetime.now().isoformat()},
]
metrics_db = [
    {"cpu": 45, "memory": 62, "disk": 78, "timestamp": datetime.now().isoformat()},
]
alerts_db = [
    {
        "id": 1,
        "title": "High CPU Usage",
        "message": "CPU usage has exceeded 80% threshold",
        "severity": "CRITICAL",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": 2,
        "title": "Memory Warning",
        "message": "Memory usage is at 75% capacity",
        "severity": "WARNING",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": 3,
        "title": "API Response Time",
        "message": "Average response time is 2.5s (normal: <500ms)",
        "severity": "INFO",
        "timestamp": datetime.now().isoformat()
    },
]

# ==================== LOGS ENDPOINTS ====================

@app.get("/logs/search")
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

@app.get("/logs/stats")
async def log_stats():
    """Get log statistics"""
    error_count = len([l for l in logs_db if l.get("level") == "ERROR"])
    warn_count = len([l for l in logs_db if l.get("level") == "WARN"])
    info_count = len([l for l in logs_db if l.get("level") == "INFO"])
    
    return {
        "total_logs": len(logs_db),
        "by_level": {
            "ERROR": error_count,
            "WARN": warn_count,
            "INFO": info_count,
            "DEBUG": 0
        }
    }

@app.post("/logs/ingest")
async def ingest_log(log_entry: dict):
    """Ingest a log entry"""
    log_entry["timestamp"] = datetime.now().isoformat()
    logs_db.append(log_entry)
    return {"status": "success", "id": len(logs_db)}

# ==================== METRICS ENDPOINTS ====================

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return {
        "cpu_usage": 0,
        "memory_usage": 0,
        "disk_usage": 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics/history")
async def metrics_history(hours: int = 24):
    """Get metrics history"""
    return {
        "hours": hours,
        "data": metrics_db[-100:],
        "total": len(metrics_db)
    }

@app.post("/metrics/record")
async def record_metric(metric: dict):
    """Record a metric"""
    metric["timestamp"] = datetime.now().isoformat()
    metrics_db.append(metric)
    return {"status": "success"}

# ==================== ALERTS ENDPOINTS ====================

@app.get("/alerts")
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

@app.post("/alerts")
async def create_alert(alert: dict):
    """Create an alert"""
    alert["id"] = len(alerts_db) + 1
    alert["timestamp"] = datetime.now().isoformat()
    alerts_db.append(alert)
    return {"status": "success", "alert_id": alert["id"]}

@app.delete("/alerts/{alert_id}")
async def dismiss_alert(alert_id: int):
    """Dismiss an alert"""
    global alerts_db
    alerts_db = [a for a in alerts_db if a.get("id") != alert_id]
    return {"status": "success", "dismissed_id": alert_id}

# ==================== UTILITY ENDPOINTS ====================

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Distributed Log Analytics Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        header { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 28px; color: #667eea; display: flex; align-items: center; gap: 10px; }
        .status-badge { display: inline-block; padding: 8px 16px; background: #10b981; color: white; border-radius: 20px; font-size: 12px; font-weight: 600; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
        .card h2 { font-size: 18px; color: #667eea; margin-bottom: 15px; }
        .metric { font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0; }
        .sub-metric { font-size: 12px; color: #999; margin: 8px 0; }
        .search-box { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .search-box input { width: 100%; padding: 12px 16px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; }
        .search-box input:focus { outline: none; border-color: #667eea; }
        .logs-section { background: white; border-radius: 10px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .logs-section h2 { color: #667eea; margin-bottom: 20px; font-size: 20px; }
        .log-entry { padding: 15px; border-left: 4px solid #667eea; background: #f9fafb; margin-bottom: 10px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        .log-time { color: #999; font-size: 12px; font-family: monospace; }
        .log-message { flex: 1; margin: 0 15px; color: #333; font-size: 14px; }
        .log-level { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
        .level-error { background: #fee2e2; color: #dc2626; }
        .level-warn { background: #fef3c7; color: #d97706; }
        .level-info { background: #dbeafe; color: #2563eb; }
        .alert { padding: 15px; border-radius: 8px; display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
        .alert-critical { background: #fee2e2; border-left: 4px solid #dc2626; }
        .alert-warning { background: #fef3c7; border-left: 4px solid #d97706; }
        .alert-info { background: #dbeafe; border-left: 4px solid #2563eb; }
        .alert-icon { font-size: 20px; flex-shrink: 0; }
        .alert-content { flex: 1; }
        .alert-title { font-weight: 600; margin-bottom: 4px; }
        .alert-message { font-size: 13px; color: #555; }
        .loading { text-align: center; padding: 20px; color: #999; }
        .spinner { border: 3px solid #f3f4f6; border-top: 3px solid #667eea; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .empty-state { text-align: center; padding: 40px; color: #999; }
        footer { text-align: center; color: white; padding: 20px; margin-top: 40px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>📊 Log Analytics Platform</h1>
                <p style="color: #999; margin-top: 5px;">Distributed log aggregation & monitoring</p>
            </div>
            <div class="status-badge" id="status">● Connecting...</div>
        </header>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search logs (e.g., 'error', 'warning')..." autocomplete="off">
        </div>
        <div class="dashboard">
            <div class="card"><h2>📝 Total Logs</h2><div class="metric" id="totalLogs">0</div><div class="sub-metric">logs ingested</div></div>
            <div class="card"><h2>⚠️ Alerts</h2><div class="metric" id="alertCount">0</div><div class="sub-metric"><span id="criticalCount">0</span> critical, <span id="warningCount">0</span> warning</div></div>
            <div class="card"><h2>📈 Metrics</h2><div class="metric" id="metricCount">0</div><div class="sub-metric">metrics recorded</div></div>
            <div class="card"><h2>✅ System Status</h2><div class="metric" id="systemStatus" style="font-size: 24px;">Healthy</div><div class="sub-metric">API is operational</div></div>
        </div>
        <div class="logs-section">
            <h2>📋 Recent Logs</h2>
            <div id="logsContainer"><div class="loading"><div class="spinner"></div><p>Loading logs...</p></div></div>
        </div>
        <div class="logs-section">
            <h2>🚨 Active Alerts</h2>
            <div id="alertsContainer"><div class="loading"><div class="spinner"></div><p>Loading alerts...</p></div></div>
        </div>
        <footer>
            <p>Distributed Log Analytics Platform • Powered by FastAPI & Vercel</p>
            <p id="apiVersion" style="margin-top: 10px;"></p>
        </footer>
    </div>
    <script>
        const API_BASE = window.location.origin;
        let allLogs = [];
        let allAlerts = [];
        async function init() {
            await Promise.all([fetchStats(), fetchLogs(), fetchAlerts(), fetchApiInfo()]);
            setInterval(fetchStats, 5000);
            setInterval(fetchLogs, 10000);
            setInterval(fetchAlerts, 10000);
        }
        async function fetchStats() {
            try {
                const [logsRes, alertsRes, metricsRes, healthRes] = await Promise.all([
                    fetch(`${API_BASE}/logs/stats`),
                    fetch(`${API_BASE}/alerts`),
                    fetch(`${API_BASE}/metrics`),
                    fetch(`${API_BASE}/health`)
                ]);
                if (logsRes.ok && alertsRes.ok && metricsRes.ok && healthRes.ok) {
                    const logsData = await logsRes.json();
                    const alertsData = await alertsRes.json();
                    document.getElementById('totalLogs').textContent = logsData.total_logs || 0;
                    document.getElementById('alertCount').textContent = alertsData.alerts?.length || 0;
                    document.getElementById('criticalCount').textContent = alertsData.critical || 0;
                    document.getElementById('warningCount').textContent = alertsData.warning || 0;
                    document.getElementById('metricCount').textContent = alertsData.alerts?.length || 0;
                    document.getElementById('status').textContent = '● Connected';
                    document.getElementById('status').style.background = '#10b981';
                } else {
                    document.getElementById('status').textContent = '● Error';
                    document.getElementById('status').style.background = '#ef4444';
                }
            } catch (error) {
                console.error('Error fetching stats:', error);
                document.getElementById('status').textContent = '● Offline';
                document.getElementById('status').style.background = '#ef4444';
            }
        }
        async function fetchLogs() {
            try {
                const res = await fetch(`${API_BASE}/logs/search`);
                if (res.ok) {
                    const data = await res.json();
                    allLogs = data.results || [];
                    renderLogs(allLogs);
                }
            } catch (error) {
                console.error('Error fetching logs:', error);
                document.getElementById('logsContainer').innerHTML = '<div class="empty-state">❌ Failed to load logs</div>';
            }
        }
        async function fetchAlerts() {
            try {
                const res = await fetch(`${API_BASE}/alerts`);
                if (res.ok) {
                    const data = await res.json();
                    allAlerts = data.alerts || [];
                    renderAlerts(allAlerts);
                }
            } catch (error) {
                console.error('Error fetching alerts:', error);
                document.getElementById('alertsContainer').innerHTML = '<div class="empty-state">❌ Failed to load alerts</div>';
            }
        }
        async function fetchApiInfo() {
            try {
                const res = await fetch(`${API_BASE}/api/info`);
                if (res.ok) {
                    const data = await res.json();
                    document.getElementById('apiVersion').textContent = `API v${data.version} • Environment: ${data.environment}`;
                }
            } catch (error) {}
        }
        function renderLogs(logs) {
            const container = document.getElementById('logsContainer');
            if (!logs || logs.length === 0) {
                container.innerHTML = '<div class="empty-state">📭 No logs yet</div>';
                return;
            }
            const html = logs.map(log => {
                const level = log.level || 'INFO';
                const levelClass = `level-${level.toLowerCase()}`;
                const timestamp = log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'N/A';
                const message = log.message || log.text || JSON.stringify(log);
                return `<div class="log-entry"><span class="log-time">${timestamp}</span><span class="log-message">${message}</span><span class="log-level ${levelClass}">${level}</span></div>`;
            }).join('');
            container.innerHTML = html;
        }
        function renderAlerts(alerts) {
            const container = document.getElementById('alertsContainer');
            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<div class="empty-state">✨ No active alerts</div>';
                return;
            }
            const icons = {'CRITICAL': '🔴', 'WARNING': '🟡', 'INFO': '🔵'};
            const html = alerts.map(alert => {
                const severity = alert.severity || 'INFO';
                const alertClass = `alert alert-${severity.toLowerCase()}`;
                const icon = icons[severity] || '⚪';
                return `<div class="${alertClass}"><div class="alert-icon">${icon}</div><div class="alert-content"><div class="alert-title">${alert.title || severity}</div><div class="alert-message">${alert.message || 'No description'}</div><div class="sub-metric">${new Date(alert.timestamp || Date.now()).toLocaleString()}</div></div></div>`;
            }).join('');
            container.innerHTML = html;
        }
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const filtered = allLogs.filter(log => {
                const message = (log.message || log.text || JSON.stringify(log)).toLowerCase();
                return message.includes(query);
            });
            renderLogs(filtered);
        });
        init();
    </script>
</body>
</html>"""

# ==================== UTILITY ENDPOINTS ====================

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the dashboard HTML"""
    return HTML_DASHBOARD
async def root():
    """Root endpoint"""
    return {
        "message": "Distributed Log Analytics Platform API",
        "status": "healthy",
        "version": "0.1.0",
        "deployment": "vercel",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
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
        "docs": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "logs": {
                "search": "GET /logs/search",
                "stats": "GET /logs/stats",
                "ingest": "POST /logs/ingest"
            },
            "metrics": {
                "current": "GET /metrics",
                "history": "GET /metrics/history",
                "record": "POST /metrics/record"
            },
            "alerts": {
                "list": "GET /alerts",
                "create": "POST /alerts",
                "dismiss": "DELETE /alerts/{id}"
            }
        }
    }

# Export the app for Vercel
__all__ = ["app"]
