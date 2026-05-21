from typing import List, Dict, Any
from jarvis.core.engine import Node

class TaskDecomposer:
    def __init__(self):
        pass

    async def decompose(self, high_level_intent: str) -> List[Dict[str, Any]]:
        """
        Convert high level intent into a list of subtasks (DAG steps).
        """
        # In production, this would use an LLM with structured output
        return [
            {"action": "search", "params": {"query": high_level_intent}},
            {"action": "summarize", "params": {}}
        ]

    def build_dag(self, subtasks: List[Dict[str, Any]]) -> List[Node]:
        """
        Convert subtasks into engine nodes with dependencies.
        """
        nodes = []
        for i, task in enumerate(subtasks):
            node = Node(name=f"Task_{i}", action_type=task["action"], payload=task["params"])
            if i > 0:
                node.dependencies.append(nodes[i-1].id)
            nodes.append(node)
        return nodes
