from fastapi import FastAPI

app = FastAPI(
    title="Distributed Log Analytics Platform",
    version="0.1.0"
)

# ---------- Root ----------
@app.get("/")
def root():
    return {"message": "Distributed Log Analytics Platform API is running 🚀"}

# ---------- Metrics ----------
@app.get("/metrics")
def get_metrics():
    return {"status": "ok", "data": "metrics coming soon"}

# ---------- Log search ----------
@app.get("/logs/search")
def search_logs(query: str = ""):
    return {"query": query, "results": []}

# ---------- Alerts ----------
@app.get("/alerts")
def get_alerts():
    return {"alerts": []}
