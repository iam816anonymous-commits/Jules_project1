from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import datetime

class WorldState(BaseModel):
    timestamp: datetime.datetime = datetime.datetime.utcnow()
    open_windows: List[Dict[str, Any]] = []
    active_apps: List[str] = []
    browser_tabs: List[Dict[str, Any]] = []
    cursor_state: Dict[str, Any] = {"x": 0, "y": 0}
    clipboard: str = ""
    focused_element: Optional[Dict[str, Any]] = None
    current_task_id: Optional[str] = None
    planner_state: Dict[str, Any] = {}
    memory_links: List[str] = []
    confidence: float = 1.0

    def snapshot(self) -> Dict[str, Any]:
        return self.model_dump()

    def update(self, delta: Dict[str, Any]):
        # Update state based on new observations
        for key, value in delta.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.timestamp = datetime.datetime.utcnow()

    def diff(self, other: 'WorldState') -> Dict[str, Any]:
        # Basic diff logic
        return {"changed_keys": []}
