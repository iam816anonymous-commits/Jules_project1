import unittest
import asyncio
from jarvis.core.engine import RuntimeGraphEngine, Node
from jarvis.core.policy import PolicyEngine, RiskLevel

class TestCore(unittest.TestCase):
    def test_policy_engine(self):
        engine = PolicyEngine()
        self.assertEqual(engine.evaluate("open_browser", {}), RiskLevel.SAFE)
        self.assertEqual(engine.evaluate("shutdown_system", {}), RiskLevel.BLOCK)
        self.assertEqual(engine.evaluate("delete_file", {}), RiskLevel.CONFIRM)

    def test_graph_engine_basic(self):
        engine = RuntimeGraphEngine()
        node1 = Node("Task 1", "search", {})
        node2 = Node("Task 2", "summarize", {})
        engine.add_node(node1)
        engine.add_node(node2)
        engine.add_dependency(node2.id, node1.id)

        executable = engine.get_executable_nodes()
        self.assertEqual(len(executable), 1)
        self.assertEqual(executable[0].id, node1.id)

if __name__ == '__main__':
    unittest.main()
