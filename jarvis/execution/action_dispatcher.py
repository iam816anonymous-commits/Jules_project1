from typing import Dict, Any
from jarvis.execution.tool_router import ToolRouter

class ActionDispatcher:
    def __init__(self, router: ToolRouter):
        self.router = router

    async def dispatch(self, action: Dict[str, Any]) -> Dict[str, Any]:
        action_name = action.get("action")
        params = action.get("params", {})

        if not action_name:
            return {"success": False, "error": "No action name provided"}

        return await self.router.route_and_execute(action_name, params)
