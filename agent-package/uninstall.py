# uninstall.py
"""
Vigilant Agent Uninstaller
"""

import sys
import subprocess
import argparse
from logger import setup_logger
import logging

logger = setup_logger(name="vigilant-uninstaller", level=logging.INFO)


class VigilantUninstaller:
    def __init__(self, force=False):
        self.force = force
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
    
    def confirm_uninstall(self):
        """Ask for confirmation"""
        if self.force:
            logger.info("Force mode - skipping confirmation")
            return True
        
        logger.info("This will remove the scheduled task.")
        logger.info("Agent files will remain in the current directory.")
        logger.info("")
        
        try:
            response = input("Continue? (yes/no): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            logger.info("")
            logger.info("No input received")
            return False
        
        if response == "yes":
            logger.info("User confirmed uninstallation")
            return True
        else:
            logger.info("User cancelled uninstallation")
            return False
    
    def stop_task(self):
        """Stop the scheduled task"""
        logger.info("Stopping scheduled task...")
        
        try:
            subprocess.run(
                ["schtasks", "/End", "/TN", self.task_name],
                capture_output=True,
                check=True
            )
            logger.info("Task stopped ✓")
        except subprocess.CalledProcessError:
            logger.info("Task not running")
        
        return True
    
    def delete_task(self):
        """Delete the scheduled task"""
        logger.info("Removing scheduled task...")
        
        try:
            subprocess.run(
                ["schtasks", "/Delete", "/TN", self.task_name, "/F"],
                check=True,
                capture_output=True
            )
            logger.info("Task removed ✓")
            return True
        except subprocess.CalledProcessError:
            logger.warning("Task not found (may already be removed)")
            return True
    
    def verify_cleanup(self):
        """Verify task was removed"""
        logger.info("Verifying cleanup...")
        
        try:
            subprocess.run(
                ["schtasks", "/Query", "/TN", self.task_name],
                capture_output=True,
                check=True
            )
            logger.warning("Task still exists")
            return False
        except subprocess.CalledProcessError:
            logger.info("Task successfully removed ✓")
            return True
    
    def uninstall(self):
        """Run uninstallation"""
        logger.info("="*60)
        logger.info("Vigilant Agent Uninstaller")
        logger.info("="*60)
        logger.info("")
        
        if not self.check_admin():
            return False
        
        if not self.confirm_uninstall():
            logger.info("Uninstallation cancelled")
            return False
        
        logger.info("")
        self.stop_task()
        self.delete_task()
        self.verify_cleanup()
        
        logger.info("")
        logger.info("="*60)
        logger.info("Uninstallation Complete")
        logger.info("="*60)
        logger.info("Scheduled task removed.")
        logger.info("Agent files remain in current directory.")
        logger.info("Delete manually if needed.")
        logger.info("="*60)
        
        return True


def main():
    parser = argparse.ArgumentParser(description="Uninstall Vigilant Agent")
    parser.add_argument("--force", action="store_true", 
                       help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    uninstaller = VigilantUninstaller(force=args.force)
    success = uninstaller.uninstall()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Uninstallation cancelled by user")
        sys.exit(1)
    except Exception:
        logger.exception("Uninstallation crashed unexpectedly")
        logger.error("This is a bug - please report it")
        sys.exit(1)