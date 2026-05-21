from typing import List, Dict, Any, Optional
from jarvis.planner.graph import GraphPlanner
import logging

logger = logging.getLogger(__name__)

class Plan:
    def __init__(self, steps: List[Dict[str, Any]], score: float):
        self.steps = steps
        self.score = score

class Planner:
    def __init__(self):
        self.graph_planner = GraphPlanner()

    async def generate_plans(self, goal: str, context: Dict[str, Any]) -> List[Plan]:
        """
        Generate grounded plans based on goal and world model context.
        """
        # Logic to decide between multiple strategies
        # Strategy A: Linear sequence
        steps_a = [{"action": "mouse_move", "params": {"x": 100, "y": 100}}]

        return [Plan(steps=steps_a, score=0.9)]

    async def select_best_plan(self, plans: List[Plan]) -> Plan:
        if not plans:
            raise ValueError("No plans generated")
        return max(plans, key=lambda p: p.score)
