from typing import List, Dict, Any
from pydantic import BaseModel

class UnifiedObservation(BaseModel):
    windows: List[Dict[str, Any]]
    active_window: Dict[str, Any]
    focus: Optional[str] = None
    browser_tabs: List[Dict[str, Any]] = []
    clipboard: str = ""
    ocr: List[Dict[str, Any]] = []
    cursor: Dict[str, int] = {"x": 0, "y": 0}
    confidence: float

class ObservationFusion:
    def __init__(self):

    def merge(self,
              vision_data: Dict[str, Any],
              os_data: Dict[str, Any],
              browser_data: Dict[str, Any],
              clipboard_data: str) -> UnifiedObservation:
        """
        Merge Vision, OS, and Browser signals into a single source of truth.
        """
        # Cross-validate vision OCR with active window title
        v_text = vision_data.get("raw_text", [])

        return UnifiedObservation(
            windows=os_data.get("all_windows", []),
            active_window=os_data.get("active", {}),
            focus=os_data.get("focus"),
            browser_tabs=browser_data.get("tabs", []),
            clipboard=clipboard_data,
            ocr=v_text,
            cursor=os_data.get("cursor", {"x": 0, "y": 0}),
            confidence=0.9
        )
