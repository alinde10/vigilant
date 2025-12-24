# install.py
"""
Vigilant Agent Installer
Creates scheduled task to run agent from current directory
"""

import sys
import subprocess
from pathlib import Path
import argparse
import json
from logger import setup_logger

PARENT_DIR_PATH = Path(__file__).parent.resolve()

logger = setup_logger()

class VigilantInstaller:
    def __init__(self, rig_id: str, server_url: str, api_key: str):
        self.rig_id = rig_id
        self.server_url = server_url
        self.api_key = api_key
        self.agent_dir = Path(__file__).parent.resolve()
        self.task_name = "VigilantAgent"
    
    def check_admin(self):
        """Check if running as administrator"""
        logger.info("Checking admin rights...")
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                logger.error("Must run as Administrator")
                logger.error("Right-click and select 'Run as Administrator'")
                return False
            logger.info("Running as Administrator ✓")
            return True
        except Exception:
            logger.warning("Could not verify admin status")
            return True
    
    def check_python_version(self):
        """Check Python version"""
        logger.info("Checking Python version...")
        version = sys.version_info
        
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            logger.error(f"Python 3.9+ required. Found: {version.major}.{version.minor}")
            return False
        
        logger.info(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    
    def check_files_exist(self):
        """Verify required files exist"""
        logger.info("Checking required files...")
        required_files = ["agent.py", "logger.py", "requirements.txt", "task_template.xml"]
        
        for filename in required_files:
            filepath = self.agent_dir / filename
            if not filepath.exists():
                logger.error(f"Missing file: {filename}")
                logger.error(f"Expected at: {filepath}")
                return False
        
        logger.info("All required files found ✓")
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        logger.info("Installing Python dependencies...")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
                capture_output=True,
                cwd=str(self.agent_dir)
            )
            logger.info("Dependencies installed ✓")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to install dependencies")
            logger.error(e.stderr.decode())
            return False
    
    def update_config(self):
        """Update config.json with installation settings"""
        logger.info("Updating configuration...")
        config_file = self.agent_dir / "config.json"
        
        # Load existing or create new config
        if config_file.exists():
            logger.debug(f"Loading existing config from {config_file}")
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Existing config has invalid JSON: {e}")
                return False
        else:
            logger.debug("Creating new config")
            config = {
                "metadata": {
                    "location": "Lab A",
                    "capabilities": ["CAN", "Ethernet"]
                },
                "test_process_names": ["CANoe.exe", "TestRunner.exe"]
            }
        
        # Update with installation values
        config["rig_id"] = self.rig_id
        config["server_url"] = self.server_url
        config["api_key"] = self.api_key
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration saved to {config_file} ✓")
        return True
    
    def test_agent(self):
        """Test agent runs successfully"""
        logger.info("Testing agent...")
        
        try:
            result = subprocess.run(
                [sys.executable, "agent.py"],
                cwd=str(self.agent_dir),
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("Agent test successful ✓")
                return True
            else:
                logger.error("Agent test failed")
                logger.error(result.stderr.decode())
                return False
        except subprocess.TimeoutExpired:
            logger.error("Agent test timed out (>30 seconds)")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Agent test error: {e}")
            return False
    
    def create_scheduled_task(self):
        """Create Windows Task Scheduler task"""
        logger.info("Creating scheduled task...")
        
        python_exe = sys.executable
        agent_script = self.agent_dir / "agent.py"
        
        # Load task template
        template_file = self.agent_dir / "task_template.xml"
        try:
            with open(template_file, 'r', encoding='utf-16') as f:
                task_xml = f.read()
        except FileNotFoundError:
            logger.error(f"Task template not found: {template_file}")
            return False
        
        # Fill in template variables
        task_xml = task_xml.format(
            rig_id=self.rig_id,
            python_exe=python_exe,
            agent_script=agent_script,
            working_dir=self.agent_dir
        )
        
        # Save filled template
        xml_file = self.agent_dir / "task_temp.xml"
        with open(xml_file, 'w', encoding='utf-16') as f:
            f.write(task_xml)
        
        try:
            # Delete existing task if present
            subprocess.run(
                ["schtasks", "/Delete", "/TN", self.task_name, "/F"],
                capture_output=True
            )
            
            # Create new task
            subprocess.run(
                ["schtasks", "/Create", "/XML", str(xml_file), "/TN", self.task_name],
                check=True,
                capture_output=True
            )
            
            logger.info(f"Scheduled task '{self.task_name}' created ✓")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to create scheduled task")
            logger.error(e.stderr.decode())
            return False
        finally:
            # Always clean up temp XML
            if xml_file.exists():
                xml_file.unlink()
    
    def start_task(self):
        """Start the scheduled task"""
        logger.info("Starting agent task...")
        
        try:
            subprocess.run(
                ["schtasks", "/Run", "/TN", self.task_name],
                check=True,
                capture_output=True
            )
            logger.info("Agent started ✓")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to start agent")
            logger.error(e.stderr.decode())
            return False
    
    def print_summary(self):
        """Log installation summary"""
        logger.info("="*60)
        logger.info("Installation Complete")
        logger.info("="*60)
        logger.info(f"Agent Directory:    {self.agent_dir}")
        logger.info(f"Rig ID:             {self.rig_id}")
        logger.info(f"Server URL:         {self.server_url}")
        logger.info(f"Task Name:          {self.task_name}")
        logger.info(f"Log Files:          {self.agent_dir / 'logs'}")
        logger.info("")
        logger.info("Useful Commands:")
        logger.info("  View logs:      type logs\\vigilant.log")
        logger.info("  Manual test:    python agent.py")
        logger.info("  Check task:     schtasks /Query /TN VigilantAgent /FO LIST")
        logger.info("  Uninstall:      python uninstall.py")
        logger.info("="*60)
    
    def install(self):
        """Run installation"""
        logger.info("="*60)
        logger.info("Vigilant Agent Installer")
        logger.info("="*60)
        logger.info(f"Rig ID:      {self.rig_id}")
        logger.info(f"Server URL:  {self.server_url}")
        logger.info(f"API Key:     {'*' * min(len(self.api_key), 20)}")
        logger.info("")
        
        # Run installation steps
        steps = [
            ("Checking admin rights", self.check_admin),
            ("Checking Python version", self.check_python_version),
            ("Checking required files", self.check_files_exist),
            ("Installing dependencies", self.install_dependencies),
            ("Updating configuration", self.update_config),
            ("Testing agent", self.test_agent),
            ("Creating scheduled task", self.create_scheduled_task),
            ("Starting agent", self.start_task),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                logger.error(f"Installation failed at: {step_name}")
                logger.error(f"Check logs: {self.agent_dir / 'logs' / 'vigilant-installer.log'}")
                return False
        
        logger.info("Installation completed successfully")
        self.print_summary()
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Install Vigilant Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py --rig-id RIG-07 --server-url https://vigilant.io --api-key abc123
  python install.py --rig-id TEST-01 --server-url http://localhost:5000 --api-key test
        """
    )
    
    parser.add_argument("--rig-id", required=True, 
                       help="Rig ID (e.g., RIG-07)")
    parser.add_argument("--server-url", required=True, 
                       help="Server URL (e.g., https://vigilant.io)")
    parser.add_argument("--api-key", required=True, 
                       help="API key for authentication")
    
    args = parser.parse_args()
    
    installer = VigilantInstaller(
        rig_id=args.rig_id,
        server_url=args.server_url,
        api_key=args.api_key
    )
    
    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Installation cancelled by user")
        sys.exit(1)
    except Exception:
        logger.exception("Installation crashed unexpectedly")
        logger.error("This is a bug - please report it")
        sys.exit(1)