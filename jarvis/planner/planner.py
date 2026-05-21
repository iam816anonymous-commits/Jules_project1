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
        Generate plans based on goal and world model context.
        """
        # Search strategy if goal contains 'search' or 'research'
        if "research" in goal.lower() or "search" in goal.lower():
            steps = [
                {"action": "open_browser", "params": {}},
                {"action": "search_web", "params": {"query": goal}},
                {"action": "summarize", "params": {}}
            ]
            return [Plan(steps=steps, score=0.95)]

        # Default fallback
        return [Plan(steps=[{"action": "chat", "params": {"message": goal}}], score=0.5)]

    async def select_best_plan(self, plans: List[Plan]) -> Plan:
        if not plans:
            raise ValueError("No plans generated")
        return max(plans, key=lambda p: p.score)
