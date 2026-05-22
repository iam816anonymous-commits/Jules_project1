from typing import Dict, Any, List

class BehaviorOptimizer:
    def __init__(self):
        self.preferences = {
            "default_search_engine": "google",
            "retry_attempts": 3,
            "tool_bias": {} # bias for specific tools based on success
        }

    def optimize(self, history: List[Any], rewards: List[float]):
        """
        Adjust planner preferences and tool bias based on historical rewards.
        """
        # Reinforcement learning-like adjustment of preferences

    def get_current_preferences(self) -> Dict[str, Any]:
        return self.preferences
