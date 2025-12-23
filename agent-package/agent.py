# agent.py
"""
Rig Monitoring Agent for Windows
Collects rig status and sends to central server
"""

import json
import requests
import psutil
import socket
import platform
from datetime import datetime, timezone
from pathlib import Path
import sys
from logger import setup_logger

CONFIG_PATH = Path(__file__).parent / "config.json"

logger = setup_logger()
logger.info("Agent starting")
logger.debug("Debug info")
logger.warning("Warning message")
logger.error("Error occurred")


class RigAgent:
    def __init__(self, config_path=CONFIG_PATH):
        """Initialize agent with config"""
        self.config = self.load_config(config_path)
        self.server_url = self.config["server_url"]
        self.api_key = self.config["api_key"]
        self.rig_id = self.config["rig_id"]
        self.metadata = self.config.get("metadata", {})

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found at {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file\n{e}")
            sys.exit(1)

    def collect_system_status(self) -> dict:
        """Collect system-level metrics"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "disk_percent": psutil.disk_usage("C:\\").percent,
                "disk_free_gb": round(psutil.disk_usage("C:\\").free / (1024**3), 2),
                "uptime_hours": round((datetime.now() - boot_time).total_seconds() / 3600, 1)
            }
        except Exception as e:
            logger.error(f"Error collecting system status\n{e}")
            return {}

    def check_test_running(self):
        """Check if HIL test software is running"""
        # Customize this based on your actual HIL software
        # Example: Check if specific process is running
        test_processes = self.config.get("test_process_names", [])

        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] in test_processes:
                    return True, proc.info["name"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return False, None

    def get_network_info(self) -> dict:
        """Get network information"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return {
                "hostname": hostname,
                "ip_address": ip_address,
            }
        except Exception as e:
            logger.error(f"Error getting network info\n{e}")
            return {
                "hostname": "unknown",
                "ip_address": "unknown",
            }

    def collect_status(self) -> dict:
        """Collect all rig status information"""
        is_testing, test_name = self.check_test_running()
        network_info = self.get_network_info()
        system_status = self.collect_system_status()

        status = {
            "rig_id": self.rig_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "busy" if is_testing else "available",
            "is_testing": is_testing,
            "test_name": test_name,
            **network_info,
            **system_status,
            **self.metadata,
            "agent_version": "1.0.0",
            "os": platform.platform(),
        }

        return status

    def send_heartbeat(self, status):
        """Send status to central server"""
        try:
            response = requests.post(
                f"{self.server_url}/api/heartbeat",
                json=status,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=15,
            )

            if response.status_code == 200:
                logger.info(f"Heartbeat sent successfully for {self.rig_id}")
                return True
            else:
                logger.error(
                    f"Server returned status {response.status_code}: {response.text}"
                )
                return False

        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to server at {self.server_url}")
            return False
        except requests.exceptions.Timeout:
            logger.error(f"Server request timed out")
            return False
        except Exception as e:
            logger.error(f"Error sending heartbeat\n{e}")
            return False

    def run(self):
        """Main execution - collect and send status once"""
        logger.info(f"HIL Agent Run at {datetime.now(timezone.utc).isoformat()}")

        try:
            status = self.collect_status()
            self.send_heartbeat(status)
        except Exception as e:
            logger.error(f"Error in agent run\n{e}")
            sys.exit(1)


if __name__ == "__main__":
    agent = RigAgent()
    agent.run()
