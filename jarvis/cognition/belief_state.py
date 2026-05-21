from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime

class Belief(BaseModel):
    subject: str
    predicate: str
    object: Any
    confidence: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class BeliefState:
    def __init__(self):
        self.beliefs: Dict[str, Belief] = {}

    def update(self, observation: Dict[str, Any]):
        """
        Update internal beliefs based on new observations.
        """
        for key, val in observation.items():
            belief = Belief(subject=key, predicate="is", object=val, confidence=1.0)
            self.beliefs[key] = belief

    def get_belief(self, subject: str) -> Optional[Belief]:
        return self.beliefs.get(subject)

    def invalidate(self, subject: str):
        if subject in self.beliefs:
            del self.beliefs[subject]
