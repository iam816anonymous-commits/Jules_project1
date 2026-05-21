from typing import Dict, Any, Tuple
from jarvis.world_model.world_state import WorldState

class ActionValidator:
    def __init__(self):
        self.min_confidence_threshold = 0.7

    def validate(self, action: Dict[str, Any], world_state: WorldState) -> Tuple[bool, str]:
        """
        Pre-execution check against the world model.
        """
        # 1. Check confidence
        if world_state.confidence < self.min_confidence_threshold:
            return False, f"World state confidence too low: {world_state.confidence}"

        # 2. Check window existence if applicable
        target_window = action.get("params", {}).get("window_title")
        if target_window:
            window_exists = any(w["title"] == target_window for w in world_state.open_windows)
            if not window_exists:
                return False, f"Target window '{target_window}' not found in world state."

        # 3. Check if task is still active
        if not world_state.current_task_id:
            return False, "No active task found in world state."

        # 4. Check focus validity for interactive actions
        if action.get("type") in ["click", "type"]:
            if not world_state.focused_element:
                # This might be acceptable depending on action params
                pass

        return True, "Valid"
