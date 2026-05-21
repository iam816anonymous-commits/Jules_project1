import unittest
from jarvis.learning.reward_engine import RewardEngine

class TestRewardTrend(unittest.TestCase):
    def test_reward_ordering(self):
        engine = RewardEngine()

        # 1. Success (Clean)
        r_success = engine.calculate_reward(success=True, duration=5.0, hallucinated=False, recovered=False)

        # 2. Success (with recovery)
        r_recovery = engine.calculate_reward(success=True, duration=10.0, hallucinated=True, recovered=True)

        # 3. Failure (Timeout)
        r_timeout = engine.calculate_reward(success=False, duration=60.0, hallucinated=False, recovered=False)

        # 4. Unsafe (Force penalty by adding unsafe param to calculate_reward if needed,
        # for now hallucination + failure is proxy)
        r_unsafe = engine.calculate_reward(success=False, duration=10.0, hallucinated=True, recovered=False)

        print(f"Success: {r_success}, Recovery: {r_recovery}, Timeout: {r_timeout}, Unsafe: {r_unsafe}")

        self.assertTrue(r_success > r_recovery)
        self.assertTrue(r_recovery > r_timeout)
        self.assertTrue(r_timeout >= r_unsafe)

if __name__ == '__main__':
    unittest.main()
