from typing import Dict, Any

class RewardEngine:
    def __init__(self):

    def calculate_reward(self,
                         success: bool,
                         duration: float,
                         hallucinated: bool,
                         recovered: bool) -> float:
        """
        Calculate scalar reward: success - speed_penalty - hallucination + recovery_bonus.
        """
        reward = 1.0 if success else -1.0

        # Speed penalty: 0.1 per 10 seconds, max 0.5
        speed_penalty = min(0.5, (duration / 10.0) * 0.1)
        reward -= speed_penalty

        if hallucinated:
            reward -= 1.0

        if recovered:
            reward += 0.5

        return max(-2.0, min(1.5, reward))
