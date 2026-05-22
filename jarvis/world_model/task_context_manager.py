from typing import Dict, Any, Optional, List

class TaskContextManager:
    def __init__(self):
        self.active_task_id: Optional[str] = None
        self.context_stack: List[Dict[str, Any]] = []

    def push_context(self, task_id: str, context: Dict[str, Any]):
        self.active_task_id = task_id
        self.context_stack.append(context)

    def pop_context(self):
        if self.context_stack:
            self.context_stack.pop()
            if self.context_stack:
                # Update active_task_id from previous context if stored there
            else:
                self.active_task_id = None

    def get_current_context(self) -> Dict[str, Any]:
        return self.context_stack[-1] if self.context_stack else {}
