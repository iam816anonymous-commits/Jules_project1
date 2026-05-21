from typing import Dict, Any, List, Optional
from jarvis.world_model.world_state import WorldState
import copy

class StateSnapshot:
    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []
        self.max_snapshots = 10

    def take_snapshot(self, world_state: WorldState, planner_state: Dict[str, Any]):
        """
        Save a point-in-time state for recovery.
        """
        snapshot = {
            "world": world_state.snapshot(),
            "planner": copy.deepcopy(planner_state),
            "timestamp": world_state.timestamp
        }
        self.snapshots.append(snapshot)
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)
        return len(self.snapshots) - 1

    def restore(self, index: int) -> Dict[str, Any]:
        if 0 <= index < len(self.snapshots):
            return self.snapshots[index]
        raise IndexError("Snapshot index out of range")

    def get_latest(self) -> Optional[Dict[str, Any]]:
        return self.snapshots[-1] if self.snapshots else None
