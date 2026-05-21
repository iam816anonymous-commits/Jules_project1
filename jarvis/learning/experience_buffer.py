from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime

class Experience(BaseModel):
    id: str
    timestamp: datetime.datetime = datetime.datetime.utcnow()
    observation: Dict[str, Any]
    goal: str
    action: Any
    result: Any
    reflection: Dict[str, Any]
    confidence: float
    reward: float = 0.0

class ExperienceBuffer:
    def __init__(self, capacity: int = 100):
        self.buffer: List[Experience] = []
        self.capacity = capacity

    def append(self, experience: Experience):
        self.buffer.append(experience)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def query(self, goal: str) -> List[Experience]:
        return [e for e in self.buffer if goal in e.goal]

    def summarize(self) -> Dict[str, Any]:
        if not self.buffer:
            return {}
        avg_reward = sum(e.reward for e in self.buffer) / len(self.buffer)
        return {"count": len(self.buffer), "avg_reward": avg_reward}

    def archive(self):
        # In production, move to long-term Postgres storage
        self.buffer = []
