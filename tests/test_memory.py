import unittest
from jarvis.memory.working import WorkingMemory
from jarvis.memory.episodic import EpisodicMemory

class TestMemory(unittest.TestCase):
    def test_working_memory(self):
        mem = WorkingMemory()
        mem.initialize("Find flights")
        self.assertEqual(mem.state.active_goal, "Find flights")
        mem.update_context("city", "London")
        self.assertEqual(mem.state.context["city"], "London")

    def test_episodic_memory(self):
        mem = EpisodicMemory()
        mem.record_episode("Goal", {"obs": 1}, "action", "result", 0.9)
        history = mem.get_recent_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].goal, "Goal")

if __name__ == '__main__':
    unittest.main()
