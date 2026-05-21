import unittest
import asyncio
from unittest.mock import MagicMock, patch
import os

# Mock UI dependencies for headless testing
with patch.dict('sys.modules', {
    'pyautogui': MagicMock(),
    'pygetwindow': MagicMock(),
    'psutil': MagicMock(),
    'playwright': MagicMock(),
    'playwright.async_api': MagicMock()
}):
    from jarvis.core.kernel import RuntimeKernel
    from jarvis.persistence.memory_store import MemoryStore

class TestEndToEnd(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_name = "test_e2e.db"
        self.kernel = RuntimeKernel()
        # Inject test DB
        self.kernel.store = MemoryStore(self.db_name)

    async def asyncTearDown(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    async def test_full_research_to_save_flow(self):
        # 1. Setup Goal
        goal = "Research autonomous agents and save notes"

        # 2. Start Kernel (mocked start to control execution)
        with patch.object(RuntimeKernel, '_orchestrate_execution', return_value=None):
            await self.kernel.start(goal, "test_session")

            # Verify Decomposition
            self.assertEqual(self.kernel.goal_manager.active_goal_id, (await self.kernel.goal_manager.goals.get(list(self.kernel.goal_manager.goals.keys())[0])).id)

            # 3. Simulate one dispatch
            node = MagicMock()
            node.id = "node_1"
            node.action_type = "mouse_move"
            node.payload = {"x": 10, "y": 10}
            node.name = "Test Move"

            await self.kernel.dispatch(node, MagicMock())

            # 4. Verify Persistence
            summary = self.kernel.store.summarize()
            self.assertEqual(summary["episode_count"], 1)

            await self.kernel.stop()

if __name__ == '__main__':
    unittest.main()
