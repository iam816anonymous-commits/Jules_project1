from typing import Dict, Any, List

class AgentMetrics:
    def __init__(self):
        self.metrics = {
            "success_rate": 0.0,
            "total_reward": 0.0,
            "recovery_rate": 0.0,
            "skill_reuse_count": 0,
            "planner_accuracy": 1.0,
            "hallucination_count": 0,
            "latency_ms": []
        }

    def record_event(self, event_type: str, value: Any):
        if event_type in self.metrics:
            if isinstance(self.metrics[event_type], list):
                self.metrics[event_type].append(value)
            else:
                # Update scalar metric

    def get_report(self) -> Dict[str, Any]:
        return self.metrics
