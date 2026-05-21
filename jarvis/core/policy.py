from enum import Enum
from typing import Dict, Any

class RiskLevel(Enum):
    SAFE = "SAFE"
    CONFIRM = "CONFIRM"
    BLOCK = "BLOCK"

class PolicyEngine:
    def __init__(self):
        self.policies = {
            "open_browser": RiskLevel.SAFE,
            "search_web": RiskLevel.SAFE,
            "read_file": RiskLevel.SAFE,
            "write_file": RiskLevel.CONFIRM,
            "delete_file": RiskLevel.CONFIRM,
            "execute_shell": RiskLevel.CONFIRM,
            "shutdown_system": RiskLevel.BLOCK,
        }

    def evaluate(self, action: str, params: Dict[str, Any]) -> RiskLevel:
        return self.policies.get(action, RiskLevel.CONFIRM)
