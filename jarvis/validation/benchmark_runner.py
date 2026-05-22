from typing import Dict, Any, List
import time
from jarvis.persistence.memory_store import MemoryStore

class BenchmarkRunner:
    def __init__(self, store: MemoryStore):
        self.store = store

    def calculate_v1_metrics(self) -> Dict[str, Any]:
        """
        Derive metrics from real execution history in the DB.
        """
        summary = self.store.summarize()
        total = summary.get("episode_count", 0)

        episodes = self.store.get_recent_episodes(limit=100)
        # Simplified success rate from reward
        successes = len([e for e in episodes if e["reward"] > 0])

        beliefs = self.store.get_beliefs()
        hallucinations = len([b for b in beliefs if b["confidence"] < 0.5])

        return {
            "success_rate": successes / len(episodes) if episodes else 0,
            "hallucination_count": hallucinations,
            "total_episodes": total
        }
