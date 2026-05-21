import asyncio
import logging
from typing import Optional, Dict, Any, List
from jarvis.cognition.cognitive_loop import CognitiveCycle
from jarvis.cognition.goal_manager import GoalManager
from jarvis.cognition.task_decomposer import TaskDecomposer
from jarvis.core.policy import PolicyEngine, RiskLevel
from jarvis.desktop.control_executor import ControlExecutor
from jarvis.desktop.browser_controller import BrowserController
from jarvis.world_model.action_validator import ActionValidator
from jarvis.persistence.memory_store import MemoryStore
from jarvis.learning.reward_engine import RewardEngine

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
        self.browser = BrowserController()
        self.reward_engine = RewardEngine()
        self.session_id: Optional[str] = None

    async def start(self, goal: str, session_id: str):
        self.active = True
        self.session_id = session_id

        goal_id = self.goal_manager.add_goal(goal)
        self.goal_manager.active_goal_id = goal_id

        subtasks = await self.decomposer.decompose(goal, self.cognitive_cycle.world_model.model_dump())
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
                await self.dispatch(node, engine)

            await asyncio.sleep(0.5)

    async def dispatch(self, node: Any, engine: Any):
        node.status = "running"
        action = {"action": node.action_type, "params": node.payload}

        start_time = asyncio.get_event_loop().time()
        result = await self.execute_action(action)
        duration = asyncio.get_event_loop().time() - start_time

        if result.get("success"):
            node.status = "completed"
            node.result = result
            reward = self.reward_engine.calculate_reward(True, duration, False, False)
        else:
            node.status = "failed"
            reward = self.reward_engine.calculate_reward(False, duration, False, False)
            await self.handle_failure(node, engine)

        self.store.save_episode({
            "id": node.id,
            "goal": self.goal_manager.goals[self.goal_manager.active_goal_id].title,
            "observation": self.cognitive_cycle.world_model.model_dump(),
            "action": action,
            "reflection": result,
            "reward": reward
        })

    async def execute_action(self, action: Dict[str, Any]) -> Any:
        action_name = action.get("action")
        params = action.get("params", {})

        risk = self.policy.evaluate(action_name, params)
        if risk == RiskLevel.BLOCK:
            return {"success": False, "error": "Blocked by policy"}

        is_valid, msg = self.validator.validate(action, self.cognitive_cycle.world_model)
        if not is_valid:
            return {"success": False, "error": f"Validation failed: {msg}"}

        try:
            # Tool Routing
            if action_name == "mouse_move":
                await self.executor.mouse_move(params.get("x"), params.get("y"))
            elif action_name == "mouse_click":
                await self.executor.mouse_click(params.get("x"), params.get("y"))
            elif action_name == "type":
                await self.executor.keyboard_type(params.get("text"))
            elif action_name == "open_browser":
                await self.browser.start()
            elif action_name == "search_web":
                await self.browser.navigate(f"https://www.google.com/search?q={params.get('query')}")
            else:
                return {"success": False, "error": f"Unsupported action type: {action_name}"}

            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def handle_failure(self, node: Any, engine: Any):
        logger.warning(f"Task {node.name} failed. No recovery implemented yet.")

    async def stop(self):
        self.active = False
        await self.cognitive_cycle.stop()
        await self.browser.stop()
        self.store.compact()
