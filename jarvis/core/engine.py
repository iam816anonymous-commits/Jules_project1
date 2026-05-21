from typing import List, Dict, Any, Optional
import asyncio
import uuid

class Node:
    def __init__(self, name: str, action_type: str, payload: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.action_type = action_type
        self.payload = payload
        self.dependencies: List[str] = []
        self.status = "pending" # pending, running, completed, failed
        self.result: Any = None

class RuntimeGraphEngine:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_dependency(self, node_id: str, dependency_id: str):
        if node_id in self.nodes and dependency_id in self.nodes:
            self.nodes[node_id].dependencies.append(dependency_id)

    def get_executable_nodes(self) -> List[Node]:
        executable = []
        for node in self.nodes.values():
            if node.status == "pending":
                if all(self.nodes[dep_id].status == "completed" for dep_id in node.dependencies):
                    executable.append(node)
        return executable
