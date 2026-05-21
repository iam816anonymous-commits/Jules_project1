from typing import List, Dict, Any
from jarvis.core.engine import Node, RuntimeGraphEngine

class TaskDecomposer:
    def __init__(self):
        pass

    async def decompose(self, high_level_intent: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Grounded decomposition: uses WorldModel context to tailor subtasks.
        """
        tasks = []
        intent = high_level_intent.lower()

        # Heuristic Grounding: Check if browser is already open
        browser_open = False
        if context:
            windows = context.get("windows", [])
            browser_open = any("chrome" in w.get("title", "").lower() for w in windows)

        if "research" in intent or "search" in intent:
            if not browser_open:
                tasks.append({"action": "open_browser", "params": {}})
            tasks.append({"action": "search_web", "params": {"query": high_level_intent}})
            tasks.append({"action": "summarize", "params": {}})

        elif "fibonacci" in intent:
            tasks.append({"action": "open_ide", "params": {"name": "VSCode"}})
            tasks.append({"action": "write_file", "params": {"filename": "fib.py", "content": "def fib(n): return n if n <= 1 else fib(n-1)+fib(n-2)"}})
            tasks.append({"action": "execute_shell", "params": {"command": "python3 fib.py"}})

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
