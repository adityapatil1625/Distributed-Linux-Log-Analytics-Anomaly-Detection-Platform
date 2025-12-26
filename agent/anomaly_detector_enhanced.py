"""
Enhanced Anomaly Detector Agent
Analyzes logs and metrics for anomalies
"""
import os
import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging
from collections import defaultdict

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
ANOMALY_THRESHOLD = int(os.getenv("ANOMALY_THRESHOLD", "5"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self):
        self.api_url = API_URL
        self.session = None
        self.error_patterns = defaultdict(int)
        self.metric_history = defaultdict(list)
        self.last_check = {}
        
    async def init_session(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def get_logs(self, limit: int = 100):
        """Get recent logs from API"""
        try:
            async with self.session.get(
                f"{self.api_url}/logs",
                params={"limit": limit},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("logs", [])
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
        return []
    
    async def get_metrics(self):
        """Get recent metrics from API"""
        try:
            async with self.session.get(
                f"{self.api_url}/metrics",
                params={"limit": 100},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("metrics", [])
        except Exception as e:
            logger.error(f"Error fetching metrics: {e}")
        return []
    
    async def send_alert(self, title: str, message: str, severity: str = "INFO"):
        """Send alert to API"""
        try:
            async with self.session.post(
                f"{self.api_url}/alerts",
                params={
                    "title": title,
                    "message": message,
                    "severity": severity
                },
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    logger.info(f"Alert sent: {title}")
                    return True
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
        return False
    
    def detect_error_spike(self, logs):
        """Detect spikes in error rates"""
        errors_by_source = defaultdict(int)
        
        for log in logs:
            if log.get("level") in ["ERROR", "CRITICAL"]:
                source = log.get("source", "unknown")
                errors_by_source[source] += 1
        
        anomalies = []
        for source, count in errors_by_source.items():
            prev_count = self.error_patterns.get(source, 0)
            
            # Detect spike (>50% increase from baseline)
            if prev_count > 0 and count > prev_count * 1.5:
                anomalies.append({
                    "type": "error_spike",
                    "source": source,
                    "previous": prev_count,
                    "current": count,
                    "increase": ((count - prev_count) / prev_count) * 100
                })
            
            # Detect threshold breach
            if count > ANOMALY_THRESHOLD:
                anomalies.append({
                    "type": "error_threshold",
                    "source": source,
                    "count": count,
                    "threshold": ANOMALY_THRESHOLD
                })
            
            self.error_patterns[source] = count
        
        return anomalies
    
    def detect_metric_anomalies(self, metrics):
        """Detect anomalies in metrics using simple statistics"""
        metric_groups = defaultdict(list)
        
        # Group metrics by name
        for metric in metrics:
            name = metric.get("name", "unknown")
            value = metric.get("value", 0)
            metric_groups[name].append(value)
        
        anomalies = []
        for name, values in metric_groups.items():
            if not values:
                continue
            
            # Calculate statistics
            avg = sum(values) / len(values)
            max_val = max(values)
            min_val = min(values)
            
            # Store history for trend analysis
            if name not in self.metric_history:
                self.metric_history[name] = []
            
            self.metric_history[name].extend(values)
            
            # Keep only last 100 values
            if len(self.metric_history[name]) > 100:
                self.metric_history[name] = self.metric_history[name][-100:]
            
            # Detect anomalies
            current = values[-1] if values else 0
            
            # Check for high values (>150% of average)
            if current > avg * 1.5 and avg > 0:
                anomalies.append({
                    "type": "high_value",
                    "metric": name,
                    "value": current,
                    "average": avg,
                    "deviation": ((current - avg) / avg) * 100
                })
            
            # Check for low values (<50% of average)
            if current < avg * 0.5 and avg > 0:
                anomalies.append({
                    "type": "low_value",
                    "metric": name,
                    "value": current,
                    "average": avg,
                    "deviation": ((current - avg) / avg) * 100
                })
        
        return anomalies
    
    def detect_pattern_anomalies(self, logs):
        """Detect unusual patterns in logs"""
        anomalies = []
        
        # Count unique sources
        sources = set()
        messages_by_level = defaultdict(list)
        
        for log in logs:
            sources.add(log.get("source", "unknown"))
            level = log.get("level", "INFO")
            messages_by_level[level].append(log.get("message", ""))
        
        # Detect new error sources
        error_count = len(messages_by_level.get("ERROR", []))
        warning_count = len(messages_by_level.get("WARN", []))
        
        if error_count > warning_count * 2:
            anomalies.append({
                "type": "error_heavy",
                "errors": error_count,
                "warnings": warning_count,
                "ratio": error_count / max(warning_count, 1)
            })
        
        # Detect repeated messages (potential issues)
        message_counts = defaultdict(int)
        for level_msgs in messages_by_level.values():
            for msg in level_msgs:
                message_counts[msg] += 1
        
        repeated = {msg: count for msg, count in message_counts.items() if count > 3}
        if repeated:
            anomalies.append({
                "type": "repeated_messages",
                "messages": repeated
            })
        
        return anomalies
    
    async def analyze(self):
        """Run anomaly detection analysis"""
        try:
            logger.info("Starting anomaly detection analysis...")
            
            # Fetch data
            logs = await self.get_logs(limit=200)
            metrics = await self.get_metrics()
            
            if not logs and not metrics:
                logger.warning("No data available for analysis")
                return
            
            # Run detectors
            error_anomalies = self.detect_error_spike(logs)
            metric_anomalies = self.detect_metric_anomalies(metrics)
            pattern_anomalies = self.detect_pattern_anomalies(logs)
            
            # Process anomalies
            all_anomalies = error_anomalies + metric_anomalies + pattern_anomalies
            
            if all_anomalies:
                logger.info(f"✓ Detected {len(all_anomalies)} anomalies")
                
                # Send alerts for critical anomalies
                for anomaly in all_anomalies:
                    await self._handle_anomaly(anomaly)
            else:
                logger.info("✓ No anomalies detected")
            
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
    
    async def _handle_anomaly(self, anomaly):
        """Handle individual anomaly"""
        atype = anomaly.get("type", "unknown")
        
        if atype == "error_spike":
            title = f"Error Spike in {anomaly.get('source')}"
            message = f"Errors increased from {anomaly.get('previous')} to {anomaly.get('current')} ({anomaly.get('increase'):.0f}%)"
            severity = "WARNING"
        
        elif atype == "error_threshold":
            title = f"Error Threshold Exceeded in {anomaly.get('source')}"
            message = f"{anomaly.get('count')} errors (threshold: {anomaly.get('threshold')})"
            severity = "CRITICAL"
        
        elif atype == "high_value":
            title = f"High {anomaly.get('metric')}"
            message = f"Value {anomaly.get('value'):.2f} is {anomaly.get('deviation'):.0f}% above average ({anomaly.get('average'):.2f})"
            severity = "WARNING"
        
        elif atype == "low_value":
            title = f"Low {anomaly.get('metric')}"
            message = f"Value {anomaly.get('value'):.2f} is {abs(anomaly.get('deviation', 0)):.0f}% below average ({anomaly.get('average'):.2f})"
            severity = "WARNING"
        
        elif atype == "error_heavy":
            title = "High Error Rate"
            message = f"{anomaly.get('errors')} errors vs {anomaly.get('warnings')} warnings (ratio: {anomaly.get('ratio'):.1f})"
            severity = "WARNING"
        
        elif atype == "repeated_messages":
            title = "Repeated Error Messages"
            messages = anomaly.get('messages', {})
            top_msg = max(messages.items(), key=lambda x: x[1])[0][:50]
            message = f"Message repeated {messages.get(top_msg, 0)} times: {top_msg}..."
            severity = "INFO"
        
        else:
            return
        
        await self.send_alert(title, message, severity)
    
    async def run(self):
        """Main loop"""
        logger.info("Starting Anomaly Detector")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Poll interval: {POLL_INTERVAL} seconds")
        logger.info(f"Anomaly threshold: {ANOMALY_THRESHOLD} errors")
        
        await self.init_session()
        
        try:
            while True:
                try:
                    await self.analyze()
                    await asyncio.sleep(POLL_INTERVAL)
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(POLL_INTERVAL)
                    
        finally:
            await self.close_session()
            logger.info("Anomaly Detector stopped")

async def main():
    """Entry point"""
    detector = AnomalyDetector()
    await detector.run()

if __name__ == "__main__":
    asyncio.run(main())
