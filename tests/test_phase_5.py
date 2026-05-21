import unittest
import asyncio
from jarvis.cognition.cognitive_loop import CognitiveCycle
from jarvis.cognition.goal_manager import GoalManager
from jarvis.cognition.task_decomposer import TaskDecomposer
from jarvis.persistence.memory_store import MemoryStore
import os

class TestPhase5(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.store = MemoryStore("test_phase5.db")

    async def asyncTearDown(self):
        if os.path.exists("test_phase5.db"):
            os.remove("test_phase5.db")

    async def test_cognitive_cycle_init(self):
        cycle = CognitiveCycle(self.store)
        self.assertFalse(cycle.active)
        self.assertIsNotNone(cycle.belief_state)

    def test_goal_hierarchy(self):
        gm = GoalManager()
        parent = gm.add_goal("Root Task")
        child = gm.add_goal("Sub Task", parent_id=parent)
        self.assertEqual(len(gm.goals), 2)
        self.assertIn(child, gm.goals[parent].children)

    async def test_task_decomposition(self):
        td = TaskDecomposer()
        tasks = await td.decompose("Setup project")
        self.assertGreater(len(tasks), 0)
        engine = td.build_dag(tasks)
        self.assertEqual(len(engine.nodes), len(tasks))

if __name__ == '__main__':
    unittest.main()
