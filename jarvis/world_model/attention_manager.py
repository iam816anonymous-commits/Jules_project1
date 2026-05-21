from typing import List, Dict, Any, Optional
import asyncio

class AttentionManager:
    def __init__(self):
        self.attention_queue: List[Dict[str, Any]] = []
        self.focus_lock: bool = False
        self.active_focus_id: Optional[str] = None

    def evaluate_saliency(self, observation: Any) -> List[Dict[str, Any]]:
        """
        Identify what matters most in the current observation.
        Priority: active task > user focus > error states > planner target.
        """
        saliency_map = []
        # TODO: Implement saliency scoring logic
        return saliency_map

    def set_focus(self, entity_id: str, lock: bool = False):
        self.active_focus_id = entity_id
        self.focus_lock = lock

    def get_priority_targets(self) -> List[str]:
        if self.active_focus_id:
            return [self.active_focus_id]
        return []
