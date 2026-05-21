from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime

class WorkingMemoryState(BaseModel):
    active_goal: str
    confidence: float
    assumptions: List[str]
    context: Dict[str, Any]
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class WorkingMemory:
    def __init__(self):
        self.state: Optional[WorkingMemoryState] = None

    def initialize(self, goal: str):
        self.state = WorkingMemoryState(
            active_goal=goal,
            confidence=1.0,
            assumptions=[],
            context={}
        )

    def update_context(self, key: str, value: Any):
        if self.state:
            self.state.context[key] = value
