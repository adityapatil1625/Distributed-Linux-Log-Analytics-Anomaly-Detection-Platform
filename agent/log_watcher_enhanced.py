"""
Enhanced Log Watcher Agent
Monitors system logs and sends to central API
"""
import os
import sys
import asyncio
import aiohttp
from datetime import datetime
import logging

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
LOG_FILE = os.getenv("LOG_FILE", "/var/log/syslog")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LogWatcher:
    def __init__(self):
        self.api_url = API_URL
        self.last_position = 0
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
    
    async def send_log(self, message: str, level: str = "INFO", source: str = "log_watcher"):
        """Send log to API"""
        try:
            async with self.session.post(
                f"{self.api_url}/logs/ingest",
                params={
                    "message": message.strip(),
                    "level": level,
                    "source": source
                },
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    self.consecutive_failures = 0
                    logger.debug(f"Log sent successfully: {message[:50]}...")
                else:
                    logger.warning(f"API returned {resp.status}")
                    self.consecutive_failures += 1
        except asyncio.TimeoutError:
            logger.error("Request timeout")
            self.consecutive_failures += 1
        except Exception as e:
            logger.error(f"Error sending log: {e}")
            self.consecutive_failures += 1
            
            # Send alert after multiple failures
            if self.consecutive_failures >= self.max_failures:
                await self.send_alert(
                    "Log Watcher Error",
                    f"Failed to send logs {self.consecutive_failures} times",
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
                else:
                    logger.warning(f"Alert failed with status {resp.status}")
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    async def read_logs(self):
        """Read system logs and send to API"""
        try:
            with open(LOG_FILE, 'r') as f:
                # Seek to last known position
                f.seek(self.last_position)
                
                # Read new logs
                batch = []
                for line in f:
                    if line.strip():
                        # Determine log level from content
                        level = self._extract_level(line)
                        batch.append((line, level))
                        
                        if len(batch) >= BATCH_SIZE:
                            await self._process_batch(batch)
                            batch = []
                
                # Process remaining logs
                if batch:
                    await self._process_batch(batch)
                
                # Save position
                self.last_position = f.tell()
                logger.debug(f"Read logs up to position {self.last_position}")
                
        except FileNotFoundError:
            logger.error(f"Log file not found: {LOG_FILE}")
            await self.send_alert(
                "Log File Not Found",
                f"Cannot access {LOG_FILE}",
                "ERROR"
            )
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
    
    async def _process_batch(self, batch):
        """Process batch of logs"""
        tasks = [
            self.send_log(message, level) 
            for message, level in batch
        ]
        await asyncio.gather(*tasks)
    
    def _extract_level(self, line: str) -> str:
        """Extract log level from line"""
        line_upper = line.upper()
        if "ERROR" in line_upper or "FAILED" in line_upper:
            return "ERROR"
        elif "WARN" in line_upper or "WARNING" in line_upper:
            return "WARN"
        elif "DEBUG" in line_upper:
            return "DEBUG"
        return "INFO"
    
    async def check_health(self):
        """Check if API is reachable"""
        try:
            async with self.session.get(
                f"{self.api_url}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    logger.info("✓ API is healthy")
                    return True
                else:
                    logger.warning(f"API unhealthy: {resp.status}")
                    return False
        except Exception as e:
            logger.error(f"Cannot reach API: {e}")
            return False
    
    async def run(self):
        """Main loop"""
        logger.info(f"Starting Log Watcher (watching {LOG_FILE})")
        logger.info(f"API URL: {self.api_url}")
        
        await self.init_session()
        
        try:
            # Check API availability
            if not await self.check_health():
                logger.error("API is not reachable. Retrying...")
            
            # Main loop
            while True:
                try:
                    await self.read_logs()
                    await asyncio.sleep(POLL_INTERVAL)
                except KeyboardInterrupt:
                    logger.info("Shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(POLL_INTERVAL)
                    
        finally:
            await self.close_session()
            logger.info("Log Watcher stopped")

async def main():
    """Entry point"""
    watcher = LogWatcher()
    await watcher.run()

if __name__ == "__main__":
    asyncio.run(main())
