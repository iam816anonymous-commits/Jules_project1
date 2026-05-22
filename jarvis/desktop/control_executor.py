import pyautogui
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ControlExecutor:
    def __init__(self):
        pass

    async def mouse_move(self, x: int, y: int):
        pyautogui.moveTo(x, y)

    async def mouse_click(self, x: int, y: int):
        pyautogui.click(x, y)

    async def keyboard_type(self, text: str):
        pyautogui.write(text)
