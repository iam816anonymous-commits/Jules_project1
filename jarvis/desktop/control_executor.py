import pyautogui
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ControlExecutor:
    def __init__(self):
        pyautogui.FAILSAFE = True

    async def mouse_move(self, x: int, y: int):
        logger.info(f"Moving mouse to ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.2)

    async def mouse_click(self, x: int = None, y: int = None, button: str = 'left'):
        logger.info(f"Clicking {button} at ({x}, {y})")
        pyautogui.click(x=x, y=y, button=button)

    async def keyboard_type(self, text: str):
        logger.info(f"Typing text: {text}")
        pyautogui.write(text, interval=0.01)

    async def keyboard_press(self, key: str):
        logger.info(f"Pressing key: {key}")
        pyautogui.press(key)

    async def scroll(self, clicks: int):
        logger.info(f"Scrolling {clicks}")
        pyautogui.scroll(clicks)

    async def clipboard_set(self, text: str):

    async def clipboard_get(self) -> str:
        return ""
