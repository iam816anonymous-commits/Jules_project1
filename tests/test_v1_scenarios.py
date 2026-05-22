import unittest
import asyncio
from unittest.mock import MagicMock, patch
import os

# Mock UI dependencies
with patch.dict('sys.modules', {
    'pyautogui': MagicMock(),
    'pygetwindow': MagicMock(),
    'psutil': MagicMock(),
    'playwright': MagicMock(),
    'playwright.async_api': MagicMock()
}):
    from jarvis.core.kernel import RuntimeKernel
    from jarvis.persistence.memory_store import MemoryStore
    from jarvis.validation.benchmark_runner import BenchmarkRunner

class TestV1Scenarios(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db_url = "sqlite:///test_v1.db"
        self.kernel = RuntimeKernel()
        self.kernel.store = MemoryStore(self.db_url)
        self.benchmark = BenchmarkRunner(self.kernel.store)

    async def asyncTearDown(self):
        if os.path.exists("test_v1.db"):
            os.remove("test_v1.db")

    async def test_research_scenario(self):
        with patch.object(RuntimeKernel, '_orchestrate_execution', return_value=None):
            await self.kernel.start("Research AI agents", "session_1")

            node = MagicMock()
            node.id = "n1"
            node.action_type = "mouse_move"
            node.payload = {"x":0, "y":0}
            node.name = "Move"

            await self.kernel.dispatch_task(node, MagicMock())

            metrics = self.benchmark.calculate_v1_metrics()
            self.assertEqual(metrics["total_episodes"], 1)

if __name__ == '__main__':
    unittest.main()
