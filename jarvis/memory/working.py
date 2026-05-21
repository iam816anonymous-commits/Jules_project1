from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime
from jarvis.persistence.memory_store import MemoryStore

class WorkingMemoryState(BaseModel):
    active_goal: str
    confidence: float
    assumptions: List[str]
    context: Dict[str, Any]
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class WorkingMemory:
    def __init__(self, store: MemoryStore):
        self.state: Optional[WorkingMemoryState] = None
        self.store = store

    def initialize(self, goal: str):
        self.state = WorkingMemoryState(
            active_goal=goal,
            confidence=1.0,
            assumptions=[],
            context={}
        )
        self._persist()

    def update_context(self, key: str, value: Any):
        if self.state:
            self.state.context[key] = value
            self._persist()

    def _persist(self):
        if self.state:
            self.store.update_belief("working_state", self.state.model_dump(), self.state.confidence)

    def get_full_state(self) -> Optional[Dict[str, Any]]:
        return self.state.model_dump() if self.state else None
