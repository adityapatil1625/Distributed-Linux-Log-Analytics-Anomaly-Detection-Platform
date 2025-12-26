"""
Enhanced Metrics Collector Agent
Collects system metrics (CPU, memory, disk) and sends to API
"""
import os
import sys
import asyncio
import aiohttp
import psutil
from datetime import datetime
import logging
import platform

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "30"))
HOSTNAME = platform.node()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.api_url = API_URL
        self.session = None
        self.consecutive_failures = 0
        self.max_failures = 5
        
    async def init_session(self):
        """Initialize aiohttp session"""
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def send_metric(self, name: str, value: float, unit: str = "", source: str = "metrics_collector"):
        """Send metric to API"""
        try:
            async with self.session.post(
                f"{self.api_url}/metrics",
                params={
                    "name": name,
                    "value": value,
                    "unit": unit,
                    "source": source,
                    "host": HOSTNAME
                },
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    self.consecutive_failures = 0
                    logger.debug(f"Metric sent: {name}={value}{unit}")
                else:
                    logger.warning(f"API returned {resp.status}")
                    self.consecutive_failures += 1
        except Exception as e:
            logger.error(f"Error sending metric: {e}")
            self.consecutive_failures += 1
            
            # Send alert after multiple failures
            if self.consecutive_failures >= self.max_failures:
                await self.send_alert(
                    "Metrics Collector Error",
                    f"Failed to send metrics {self.consecutive_failures} times",
                    "WARNING"
                )
    
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
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    def collect_cpu_metrics(self):
        """Collect CPU metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            return {
                "cpu_usage": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
            }
        except Exception as e:
            logger.error(f"Error collecting CPU metrics: {e}")
            return {}
    
    def collect_memory_metrics(self):
        """Collect memory metrics"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "memory_total": memory.total,
                "memory_used": memory.used,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_percent": swap.percent
            }
        except Exception as e:
            logger.error(f"Error collecting memory metrics: {e}")
            return {}
    
    def collect_disk_metrics(self):
        """Collect disk metrics"""
        try:
            disk = psutil.disk_usage('/')
            
            return {
                "disk_total": disk.total,
                "disk_used": disk.used,
                "disk_percent": disk.percent,
                "disk_free": disk.free
            }
        except Exception as e:
            logger.error(f"Error collecting disk metrics: {e}")
            return {}
    
    def collect_network_metrics(self):
        """Collect network metrics"""
        try:
            net_io = psutil.net_io_counters()
            
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            }
        except Exception as e:
            logger.error(f"Error collecting network metrics: {e}")
            return {}
    
    def collect_process_metrics(self):
        """Collect process count"""
        try:
            return {
                "process_count": len(psutil.pids())
            }
        except Exception as e:
            logger.error(f"Error collecting process metrics: {e}")
            return {}
    
    async def check_thresholds(self):
        """Check if any metrics exceed thresholds and send alerts"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            if cpu > 80:
                await self.send_alert(
                    f"High CPU Usage",
                    f"CPU usage is {cpu}%",
                    "WARNING"
                )
            
            if memory > 85:
                await self.send_alert(
                    f"High Memory Usage",
                    f"Memory usage is {memory}%",
                    "WARNING"
                )
            
            if disk > 90:
                await self.send_alert(
                    f"Low Disk Space",
                    f"Disk usage is {disk}%",
                    "CRITICAL"
                )
        except Exception as e:
            logger.error(f"Error checking thresholds: {e}")
    
    async def collect_all(self):
        """Collect all metrics and send to API"""
        try:
            # Collect all metrics
            cpu_metrics = self.collect_cpu_metrics()
            memory_metrics = self.collect_memory_metrics()
            disk_metrics = self.collect_disk_metrics()
            network_metrics = self.collect_network_metrics()
            process_metrics = self.collect_process_metrics()
            
            # Send all metrics asynchronously
            tasks = []
            
            # CPU metrics
            for key, value in cpu_metrics.items():
                if key == "cpu_usage":
                    tasks.append(self.send_metric(f"{key}", value, "%"))
                elif key == "cpu_freq":
                    tasks.append(self.send_metric(f"{key}", value, "MHz"))
                else:
                    tasks.append(self.send_metric(f"{key}", value))
            
            # Memory metrics
            for key, value in memory_metrics.items():
                if "percent" in key:
                    tasks.append(self.send_metric(f"{key}", value, "%"))
                else:
                    tasks.append(self.send_metric(f"{key}", value, "bytes"))
            
            # Disk metrics
            for key, value in disk_metrics.items():
                if "percent" in key:
                    tasks.append(self.send_metric(f"{key}", value, "%"))
                else:
                    tasks.append(self.send_metric(f"{key}", value, "bytes"))
            
            # Process count
            for key, value in process_metrics.items():
                tasks.append(self.send_metric(f"{key}", value))
            
            # Execute all tasks
            await asyncio.gather(*tasks)
            
            # Check thresholds
            await self.check_thresholds()
            
            logger.info("✓ Metrics collection complete")
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
    
    async def run(self):
        """Main loop"""
        logger.info("Starting Metrics Collector")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"Hostname: {HOSTNAME}")
        logger.info(f"Poll interval: {POLL_INTERVAL} seconds")
        
        await self.init_session()
        
        try:
            while True:
                try:
                    await self.collect_all()
                    await asyncio.sleep(POLL_INTERVAL)
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(POLL_INTERVAL)
                    
        finally:
            await self.close_session()
            logger.info("Metrics Collector stopped")

async def main():
    """Entry point"""
    collector = MetricsCollector()
    await collector.run()

if __name__ == "__main__":
    asyncio.run(main())
