from typing import List, Dict, Any
import datetime

class EpisodeRecord:
    def __init__(self, goal: str, observation: Dict[str, Any], action: Any, result: Any, confidence: float):
        self.timestamp = datetime.datetime.utcnow()
        self.goal = goal
        self.observation = observation
        self.action = action
        self.result = result
        self.confidence = confidence

class EpisodicMemory:
    def __init__(self):
        self.history: List[EpisodeRecord] = []

    def record_episode(self, goal: str, observation: Dict[str, Any], action: Any, result: Any, confidence: float):
        record = EpisodeRecord(goal, observation, action, result, confidence)
        self.history.append(record)
        return record

    def get_recent_history(self, limit: int = 10) -> List[EpisodeRecord]:
        return self.history[-limit:]
