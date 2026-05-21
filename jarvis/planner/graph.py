from typing import List, Dict, Any
from jarvis.core.engine import Node, RuntimeGraphEngine

class SynthesisNode(Node):
    def __init__(self, name: str, node_ids_to_synthesize: List[str]):
        super().__init__(name, "synthesis", {"target_nodes": node_ids_to_synthesize})

class GraphPlanner:
    def __init__(self):
        self.engine = RuntimeGraphEngine()

    def build_dependency_graph(self, goal: str, basic_steps: List[Dict[str, Any]]) -> RuntimeGraphEngine:
        """
        Convert a linear list of steps into a dependency graph.
        """
        # Simple heuristic: sequence everything
        previous_node_id = None
        for step in basic_steps:
            node = Node(name=step["action"], action_type=step["action"], payload=step)
            self.engine.add_node(node)
            if previous_node_id:
                self.engine.add_dependency(node.id, previous_node_id)
            previous_node_id = node.id

        return self.engine

    def inject_synthesis_node(self, target_node_ids: List[str], final_node_id: str):
        """
        Add a synthesis node that combines results from multiple branches.
        """
        s_node = SynthesisNode("Synthesize Results", target_node_ids)
        self.engine.add_node(s_node)
        for t_id in target_node_ids:
            self.engine.add_dependency(s_node.id, t_id)

        self.engine.add_dependency(final_node_id, s_node.id)
