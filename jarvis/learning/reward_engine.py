from typing import Dict, Any

class RewardEngine:
    def __init__(self):
        self.weights = {
            "success": 1.0,
            "recovery": 0.5,
            "speed_bonus": 0.2,
            "hallucination_penalty": -1.0,
            "unsafe_penalty": -2.0,
            "timeout_penalty": -0.5
        }

    def calculate_reward(self, outcome: Dict[str, Any], performance: Dict[str, Any]) -> float:
        """
        Calculate scalar reward based on outcome and performance metrics.
        """
        reward = 0.0

        if outcome.get("success"):
            reward += self.weights["success"]

        if outcome.get("recovered"):
            reward += self.weights["recovery"]

        if outcome.get("hallucinated"):
            reward += self.weights["hallucination_penalty"]

        if performance.get("is_fast"):
            reward += self.weights["speed_bonus"]

        if performance.get("unsafe"):
            reward += self.weights["unsafe_penalty"]

        return max(-2.0, min(1.5, reward))
