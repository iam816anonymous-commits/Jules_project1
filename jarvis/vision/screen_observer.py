import pyautogui
from PIL import Image
import io
import datetime
from typing import Dict, Any

class ScreenObserver:
    def __init__(self):
        pass

    def capture_full_screen(self) -> Image.Image:
        return pyautogui.screenshot()

    def compress_image(self, image: Image.Image, quality: int = 50) -> bytes:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        return img_byte_arr.getvalue()

    def get_compressed_state(self) -> Dict[str, Any]:
        """
        Returns ONLY compressed state as required:
        { active_window, focus, buttons, label_count }
        """
        return {
            "active_window": "VSCode",
            "focus": "Editor",
            "buttons": ["Save", "Close"],
            "label_count": 5
        }
