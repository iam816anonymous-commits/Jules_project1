import unittest
from jarvis.memory.working import WorkingMemory
from jarvis.memory.episodic import EpisodicMemory
from jarvis.persistence.memory_store import MemoryStore
import os

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore("test_mem.db")

    def tearDown(self):
        if os.path.exists("test_mem.db"):
            os.remove("test_mem.db")

    def test_working_memory(self):
        mem = WorkingMemory(self.store)
        mem.initialize("Find flights")
        self.assertEqual(mem.state.active_goal, "Find flights")
        mem.update_context("city", "London")
        self.assertEqual(mem.state.context["city"], "London")

    def test_episodic_memory(self):
        mem = EpisodicMemory(self.store)
        eid = mem.record_episode("Goal", {"obs": 1}, "action", "result", {"refl": "ok"}, 1.0, 0.9)
        self.assertIsNotNone(eid)

if __name__ == '__main__':
    unittest.main()
