from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserSchema(BaseModel):
    username: str

class EpisodeSchema(BaseModel):
    goal: str
    state: Dict[str, Any]
    confidence: float
    assistant_output: str

class ToolCallSchema(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class RuntimeState(BaseModel):
    active_goal: str
    confidence: float
    assumptions: List[str]
    context: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
