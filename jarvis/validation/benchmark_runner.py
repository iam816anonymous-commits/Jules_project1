from typing import Dict, Any, List
import time

class BenchmarkRunner:
    def __init__(self):
        self.stats = {
            "task_completion": [],
            "latency": [],
            "recovery_success": [],
            "hallucination_detected": 0
        }

    def record_task_result(self, success: bool, duration: float):
        self.stats["task_completion"].append(success)
        self.stats["latency"].append(duration)

    def get_summary(self) -> Dict[str, Any]:
        success_rate = sum(self.stats["task_completion"]) / len(self.stats["task_completion"]) if self.stats["task_completion"] else 0
        avg_latency = sum(self.stats["latency"]) / len(self.stats["latency"]) if self.stats["latency"] else 0
        return {
            "success_rate": success_rate,
            "avg_latency": avg_latency,
            "total_tasks": len(self.stats["task_completion"])
        }
