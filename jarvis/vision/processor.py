from typing import List, Dict, Any

class OCREngine:
    def extract_text(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        return [{"text": "Hello Jarvis", "bounds": (0, 0, 100, 20)}]

class UIDetector:
    def detect(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        return [{"type": "button", "label": "Click Me", "bounds": (200, 200, 50, 30)}]

class SceneGraph:
    def build(self, elements: List[Dict[str, Any]]):
        return {"root": elements}

class VisualMemory:
    def __init__(self):
        self.history = []

    def store_frame(self, frame_hash: str, analysis: Dict[str, Any]):
        self.history.append({"hash": frame_hash, "analysis": analysis})
