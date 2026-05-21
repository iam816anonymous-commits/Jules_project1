import logging
import json
import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

    def log_event(self, event_type: str, payload: Dict[str, Any]):
        event = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event_type": event_type,
            "payload": payload
        }
        self.logger.info(json.dumps(event))

class RuntimeTrace:
    def __init__(self):
        self.traces = []

    def add_trace(self, step: str, data: Any):
        self.traces.append({
            "step": step,
            "data": data,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
