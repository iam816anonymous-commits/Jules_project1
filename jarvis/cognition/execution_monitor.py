import time
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ExecutionMonitor:
    def __init__(self):
        self.running_tasks: Dict[str, float] = {}
        self.task_timeouts = {
            "default": 30.0,
            "search": 60.0
        }

    def start_task(self, task_id: str, task_type: str = "default"):
        self.running_tasks[task_id] = time.time()
        logger.info(f"Monitor: Started task {task_id} ({task_type})")

    def stop_task(self, task_id: str):
        if task_id in self.running_tasks:
            duration = time.time() - self.running_tasks[task_id]
            logger.info(f"Monitor: Stopped task {task_id} after {duration:.2f}s")
            del self.running_tasks[task_id]

    def check_for_stalls(self) -> List[str]:
        stalled_tasks = []
        now = time.time()
        for tid, start_time in self.running_tasks.items():
            if now - start_time > self.task_timeouts["default"]:
                stalled_tasks.append(tid)
        return stalled_tasks

    def record_retry(self, task_id: str, error: str):
        logger.warning(f"Monitor: Task {task_id} retrying due to {error}")
