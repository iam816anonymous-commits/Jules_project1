import psutil
from typing import Dict, Any
class DeviceManager:
    def get_system_stats(self) -> Dict[str, Any]:
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
        }
