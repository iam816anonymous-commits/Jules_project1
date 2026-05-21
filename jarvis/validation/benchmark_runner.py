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
        cursor = self.store.conn.cursor()

        # 1. Completion Rate
        cursor.execute("SELECT COUNT(*) FROM episodes WHERE reflection LIKE '%success\": true%'")
        successes = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM episodes")
        total = cursor.fetchone()[0]

        # 2. Avg Reward
        cursor.execute("SELECT AVG(reward) FROM episodes")
        avg_reward = cursor.fetchone()[0] or 0.0

        # 3. Hallucination Count (Proxy by low belief confidence in history)
        cursor.execute("SELECT COUNT(*) FROM beliefs WHERE confidence < 0.5")
        hallucinations = cursor.fetchone()[0]

        return {
            "success_rate": successes / total if total > 0 else 0,
            "avg_reward": avg_reward,
            "hallucination_count": hallucinations,
            "total_episodes": total
        }
