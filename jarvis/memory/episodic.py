from typing import List, Dict, Any, Optional
import datetime
import uuid
from jarvis.persistence.memory_store import MemoryStore

class EpisodicMemory:
    def __init__(self, store: MemoryStore):
        self.store = store

    def record_episode(self, goal: str, observation: Dict[str, Any], action: Any, result: Any, reflection: Dict[str, Any], reward: float, confidence: float):
        episode_id = str(uuid.uuid4())
        data = {
            "id": episode_id,
            "goal": goal,
            "observation": observation,
            "action": action,
            "reflection": reflection,
            "reward": reward,
            "confidence": confidence
        }
        self.store.save_episode(data)
        return episode_id
