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

        goal_id = self.goal_manager.add_goal(goal)
        self.goal_manager.active_goal_id = goal_id

        subtasks = await self.decomposer.decompose(goal)
        dag = self.decomposer.build_dag(subtasks)

        asyncio.create_task(self.cognitive_cycle.start())

        await self._orchestrate_execution(dag)

    async def _orchestrate_execution(self, engine: Any):
        while self.active:
            executable = engine.get_executable_nodes()
            if not executable:
                if all(n.status == "completed" for n in engine.nodes.values()):
                    logger.info("Goal achieved.")
                    await self.stop()
                    break
                await asyncio.sleep(1)
                continue

            for node in executable:
                node.status = "running"
                result = await self.execute_action({"action": node.action_type, "params": node.payload})
                if result.get("success"):
                    node.status = "completed"
                    node.result = result
                else:
                    node.status = "failed"
                    logger.error(f"Task {node.name} failed: {result.get('error')}")

            await asyncio.sleep(0.5)

    async def stop(self):
        self.active = False
        await self.cognitive_cycle.stop()

    async def execute_action(self, action: Dict[str, Any]) -> Any:
        action_name = action.get("action")
        params = action.get("params", {})

        # 1. Policy check
        risk = self.policy.evaluate(action_name, params)
        if risk == RiskLevel.BLOCK:
            return {"success": False, "error": "Blocked by policy"}

        # 2. Validation against World Model
        is_valid, msg = self.validator.validate(action, self.cognitive_cycle.world_model)
        if not is_valid:
            return {"success": False, "error": f"Validation failed: {msg}"}

        # 3. Execution
        try:
            if action_name == "mouse_move":
                await self.executor.mouse_move(params.get("x"), params.get("y"))
            elif action_name == "mouse_click":
                await self.executor.mouse_click(params.get("x"), params.get("y"))
            elif action_name == "type":
                await self.executor.keyboard_type(params.get("text"))
            # Add other tools...

            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
