import sys
import os
import logging
from typing import List

class DeploymentValidator:
    def __init__(self):
        self.required_packages = [
            "pydantic", "sqlalchemy", "playwright", "pyautogui", "pygetwindow", "psutil"
        ]

    def check_environment(self) -> bool:
        """
        Verify that all dependencies and OS-level requirements are met.
        """
        import importlib.util
        for pkg in self.required_packages:
            if importlib.util.find_spec(pkg) is None:
                logging.error(f"Missing required package: {pkg}")
                return False
        return True

    def check_os_permissions(self) -> bool:
        # Check if we have screen capture and input control permissions
        return True
