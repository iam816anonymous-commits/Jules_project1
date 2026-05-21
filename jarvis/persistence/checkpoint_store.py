import json
import os
from typing import Dict, Any

class CheckpointStore:
    def __init__(self, storage_dir: str = "checkpoints/"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def save_checkpoint(self, checkpoint_id: str, state: Dict[str, Any]):
        path = os.path.join(self.storage_dir, f"{checkpoint_id}.json")
        with open(path, 'w') as f:
            json.dump(state, f)

    def load_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        path = os.path.join(self.storage_dir, f"{checkpoint_id}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
