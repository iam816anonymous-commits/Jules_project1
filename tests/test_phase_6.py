import unittest
from jarvis.learning.reward_engine import RewardEngine
from jarvis.learning.skill_library import Skill, SkillLibrary
from jarvis.learning.mistake_tracker import MistakeTracker

class TestPhase6(unittest.TestCase):
    def test_reward_calculation(self):
        engine = RewardEngine()
        reward = engine.calculate_reward(success=True, duration=5.0, hallucinated=False, recovered=False)
        self.assertGreater(reward, 0.5)

    def test_skill_library(self):
        lib = SkillLibrary()
        skill = Skill("test_skill", [{"action": "click"}])
        lib.save_skill(skill)
        retrieved = lib.get_skill("test_skill")
        self.assertEqual(retrieved.name, "test_skill")

    def test_mistake_tracker(self):
        tracker = MistakeTracker()
        tracker.record_mistake("hallucination", {"goal": "test"}, "planner_drift")
        report = tracker.analyze_patterns()
        self.assertEqual(report["total"], 1)

if __name__ == '__main__':
    unittest.main()
