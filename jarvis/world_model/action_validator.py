from typing import Dict, Any, Tuple
from jarvis.world_model.world_state import WorldState

class ActionValidator:
    def __init__(self):
        self.min_confidence_threshold = 0.8
        self.locked = False # User lock for critical actions

    def validate(self, action: Dict[str, Any], world_state: WorldState) -> Tuple[bool, str]:
        """
        Grounded validation: window existence, confidence, focus, and user lock.
        """
        # 1. User Lock Check
        if self.locked:
            return False, "System is locked by user"

        # 2. Confidence Check
        if world_state.confidence < self.min_confidence_threshold:
            return False, f"World state confidence ({world_state.confidence}) below threshold ({self.min_confidence_threshold})"

        # 3. Grounding: Window & Element Existence
        params = action.get("params", {})
        target_window = params.get("window_title")
        if target_window:
            window_found = any(target_window in w.get("title", "") for w in world_state.open_windows)
            if not window_found:
                return False, f"Target window '{target_window}' not found in active desktop"

        # 4. Focus Validation
        if action.get("action") in ["mouse_click", "type"]:
            if not world_state.focused_element:
                return False, "No focused element for interactive action"

        return True, "Valid"

    def set_lock(self, locked: bool):
        self.locked = locked
