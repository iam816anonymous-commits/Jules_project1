from typing import Dict, Any, List

class CapabilityMapper:
    def __init__(self):
        # Maps action names to internal capability definitions
        self.map = {
            "open_browser": "browser:start",
            "search_web": "browser:navigate",
            "extract_notes": "browser:extract",
            "mouse_move": "os:mouse",
            "mouse_click": "os:click",
            "type": "os:keyboard",
            "save_file": "fs:write",
            "open_editor": "os:app"
        }

    def get_capability(self, action: str) -> str:
        return self.map.get(action, "unknown")
