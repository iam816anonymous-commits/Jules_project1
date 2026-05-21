from typing import List, Dict, Any
from jarvis.core.engine import Node, RuntimeGraphEngine

class TaskDecomposer:
    def __init__(self):
        pass

    async def decompose(self, high_level_intent: str) -> List[Dict[str, Any]]:
        """
        Convert high level intent into a list of structured subtasks.
        """
        # Dynamic mapping based on intent keywords (v1 heuristic)
        tasks = []
        if "research" in high_level_intent.lower():
            tasks = [
                {"action": "open_browser", "params": {}},
                {"action": "search_web", "params": {"query": high_level_intent}},
                {"action": "summarize", "params": {}}
            ]
        elif "fibonacci" in high_level_intent.lower():
            tasks = [
                {"action": "open_ide", "params": {"name": "VSCode"}},
                {"action": "write_file", "params": {"filename": "fib.py", "content": "def fib(n)..."}},
                {"action": "execute_shell", "params": {"command": "python3 fib.py"}}
            ]
        else:
            tasks = [{"action": "chat", "params": {"message": "Intent not mapped"}}]

        return tasks

    def build_dag(self, subtasks: List[Dict[str, Any]]) -> RuntimeGraphEngine:
        engine = RuntimeGraphEngine()
        prev_id = None
        for i, t in enumerate(subtasks):
            node = Node(name=f"Task_{i}_{t['action']}", action_type=t['action'], payload=t['params'])
            engine.add_node(node)
            if prev_id:
                engine.add_dependency(node.id, prev_id)
            prev_id = node.id
        return engine
