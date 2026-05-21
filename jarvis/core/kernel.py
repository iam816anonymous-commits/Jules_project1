import asyncio
import logging
from typing import Optional, Dict, Any, List
from jarvis.cognition.cognitive_loop import CognitiveCycle
from jarvis.cognition.goal_manager import GoalManager
from jarvis.cognition.task_decomposer import TaskDecomposer
from jarvis.core.policy import PolicyEngine, RiskLevel
from jarvis.desktop.control_executor import ControlExecutor
from jarvis.world_model.action_validator import ActionValidator
from jarvis.persistence.memory_store import MemoryStore

logger = logging.getLogger(__name__)

class RuntimeKernel:
    def __init__(self):
        self.active = False
        self.store = MemoryStore()
        self.cognitive_cycle = CognitiveCycle(self.store)
        self.goal_manager = GoalManager()
        self.decomposer = TaskDecomposer()
        self.policy = PolicyEngine()
        self.validator = ActionValidator()
        self.executor = ControlExecutor()
        self.session_id: Optional[str] = None

    async def start(self, goal: str, session_id: str):
        self.active = True
        self.session_id = session_id

        # 1. Initialize Goal
        goal_id = self.goal_manager.add_goal(goal)
        self.goal_manager.active_goal_id = goal_id

        # 2. Decompose Goal into subtasks
        subtasks = await self.decomposer.decompose(goal)
        dag = self.decomposer.build_dag(subtasks)

        # 3. Start Cognitive Loop
        asyncio.create_task(self.cognitive_cycle.start())

        await self._orchestrate_execution(dag)

    async def _orchestrate_execution(self, dag: Any):
        while self.active:
            await asyncio.sleep(1)

    async def stop(self):
        self.active = False
        await self.cognitive_cycle.stop()

    async def execute_action(self, action: Dict[str, Any]) -> Any:
        risk = self.policy.evaluate(action.get("action"), action.get("params", {}))
        if risk == RiskLevel.BLOCK:
            raise PermissionError(f"Action blocked by policy: {action.get('action')}")

        is_valid, msg = self.validator.validate(action, self.cognitive_cycle.world_model)
        if not is_valid:
            logger.warning(f"Validation failed: {msg}")
            return {"success": False, "error": msg}

        return {"success": True}
