from typing import List, Dict, Any, Optional

class ASR:
    async def transcribe(self, audio: bytes) -> str:
        return ""

class TTS:
    async def synthesize(self, text: str) -> bytes:
        return b""

class WakeEngine:
    def detect(self, chunk: bytes) -> bool:
        return False

class DialogManager:
    def __init__(self):
        self.context = {}

    def process_input(self, text: str) -> str:
        return f"Acknowledged: {text}"

class ConversationMemory:
    def __init__(self):
        self.turns = []

    def add_turn(self, speaker: str, text: str):
        self.turns.append({"speaker": speaker, "text": text})
