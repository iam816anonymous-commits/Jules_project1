from typing import List, Dict, Any, Optional
import uuid

class DesktopNode:
    def __init__(self, node_type: str, title: str, bounds: tuple, parent_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.type = node_type # browser, window, tab, editor, button
        self.title = title
        self.bounds = bounds # (x, y, w, h)
        self.parent_id = parent_id
        self.children: List[str] = []
        self.state: Dict[str, Any] = {}
        self.focus: bool = False
        self.confidence: float = 1.0

class DesktopGraph:
    def __init__(self):
        self.nodes: Dict[str, DesktopNode] = {}
        self.root_id: Optional[str] = None

    def add_node(self, node: DesktopNode):
        self.nodes[node.id] = node
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].children.append(node.id)
        elif not self.root_id:
            self.root_id = node.id

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            if node.parent_id and node.parent_id in self.nodes:
                self.nodes[node.parent_id].children.remove(node_id)
            # Recursively remove children?
            del self.nodes[node_id]

    def update_focus(self, focused_node_id: str):
        for node in self.nodes.values():
            node.focus = (node.id == focused_node_id)

    def find_by_title(self, title: str) -> List[DesktopNode]:
        return [n for n in self.nodes.values() if title in n.title]
