from typing import Dict, Any, Callable, Optional

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func

    def get_tool(self, name: str) -> Optional[Callable]:
        return self.tools.get(name)

class ToolRouter:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def route_and_execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.registry.get_tool(action)
        if not tool:
            return {"success": False, "error": f"Unhandled action: {action}"}

        try:
            result = await tool(**params)
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
