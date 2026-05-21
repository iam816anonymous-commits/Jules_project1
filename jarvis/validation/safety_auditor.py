from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SafetyAuditor:
    def __init__(self, policy_engine: Any):
        self.policy_engine = policy_engine
        self.violations = []

    def audit_action(self, action: str, params: Dict[str, Any], world_state: Any) -> bool:
        """
        Post-hoc or real-time safety audit of agent actions.
        """
        # 1. Check policy level
        risk = self.policy_engine.evaluate(action, params)

        # 2. Check focus grounding
        if action in ["click", "type"] and not world_state.focused_element:
            logger.warning(f"SafetyAudit: Action '{action}' attempted without focused element.")

        # 3. Check for destructive patterns
        if action == "execute_shell" and "rm -rf /" in params.get("command", ""):
            self.violations.append(action)
            return False

        return True

    def get_audit_report(self) -> Dict[str, Any]:
        return {"violations_count": len(self.violations), "violations": self.violations}
