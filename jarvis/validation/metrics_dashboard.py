from typing import Dict, Any
from jarvis.core.kernel import RuntimeKernel

class MetricsDashboard:
    def __init__(self, kernel: RuntimeKernel):
        self.kernel = kernel

    def get_realtime_stats(self) -> Dict[str, Any]:
        """
        Aggregation logic for the UI dashboard.
        """
        return {
            "kernel_active": self.kernel.active,
            "belief_count": len(self.kernel.cognitive_cycle.belief_state.beliefs),
            "goal_id": self.kernel.goal_manager.active_goal_id,
            "confidence": self.kernel.cognitive_cycle.world_model.confidence,
            "skills_loaded": 0 # TODO: fetch from skill library
        }
