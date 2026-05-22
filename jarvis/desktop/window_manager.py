import pygetwindow as gw
import psutil
from typing import List, Dict, Any

class WindowManager:
    def __init__(self):

    def get_active_window(self) -> Dict[str, Any]:
        win = gw.getActiveWindow()
        if win:
            return {
                "title": win.title,
                "box": (win.left, win.top, win.width, win.height)
            }
        return {}

    def list_windows(self) -> List[Dict[str, Any]]:
        return [{"title": w.title} for w in gw.getAllWindows()]

    def focus_window(self, title: str):
        wins = gw.getWindowsWithTitle(title)
        if wins:
            wins[0].activate()
