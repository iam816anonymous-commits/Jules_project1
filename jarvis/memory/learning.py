from typing import List, Dict, Any, Optional

class LearningMemory:
    def __init__(self):
        self.lessons: List[Dict[str, Any]] = []

    def record_learning(self, goal: str, tool: str, failure: str, repair: str, outcome: str, confidence: float):
        lesson = {
            "goal": goal,
            "tool": tool,
            "failure": failure,
            "repair": repair,
            "outcome": outcome,
            "confidence": confidence
        }
        self.lessons.append(lesson)

    def get_relevant_lessons(self, goal: str) -> List[Dict[str, Any]]:
        # In production, use semantic search to find relevant lessons
        return [l for l in self.lessons if goal in l["goal"]]

class ProceduralMemory:
    def __init__(self):
        self.workflows: Dict[str, List[Dict[str, Any]]] = {}

    def store_workflow(self, task: str, steps: List[Dict[str, Any]], outcome: str):
        if outcome == "success":
            self.workflows[task] = steps

    def get_workflow(self, task: str) -> Optional[List[Dict[str, Any]]]:
        return self.workflows.get(task)
