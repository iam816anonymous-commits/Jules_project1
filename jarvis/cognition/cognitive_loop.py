import asyncio
import logging
from typing import Optional, Dict, Any
from jarvis.world_model.world_state import WorldState
from jarvis.cognition.belief_state import BeliefState
from jarvis.persistence.memory_store import MemoryStore
from jarvis.vision.observer import VisionObserver
from jarvis.desktop.window_manager import WindowManager
from jarvis.world_model.observation_fusion import ObservationFusion

logger = logging.getLogger(__name__)

class CognitiveCycle:
    def __init__(self, store: MemoryStore):
        self.active = False
        self.belief_state = BeliefState()
        self.world_model = WorldState()
        self.store = store
        self.vision = VisionObserver()
        self.window_manager = WindowManager()
        self.fusion = ObservationFusion()

    async def start(self):
        self.active = True
        logger.info("CognitiveCycle started")
        while self.active:
            await self.tick()
            await asyncio.sleep(0.5)

    async def tick(self):
        try:
            # 1. Real Perception
            vision_obs = self.vision.observe()
            os_obs = {
                "active": self.window_manager.get_active_window(),
                "all_windows": self.window_manager.list_windows(),
                "cursor": {"x": 0, "y": 0} # Mocked cursor for now
            }

            # 2. Fusion
            unified = self.fusion.merge(
                vision_obs,
                os_obs,
                {"tabs": []}, # Browser stub
                "" # Clipboard stub
            )

            # 3. Update Beliefs & World Model
            self.belief_state.update(unified.model_dump())
            self.world_model.update(unified.model_dump())

            # 4. Persist
            belief_data = {k: v.model_dump() for k, v in self.belief_state.beliefs.items()}
            self.store.update_belief("cycle_state", belief_data, unified.confidence)

            logger.debug(f"Tick completed. Belief count: {len(self.belief_state.beliefs)}")

        except Exception as e:
            logger.error(f"Error in cognitive tick: {e}")
            await self.recover(e)

    async def stop(self):
        self.active = False

    async def recover(self, error: Exception):
        logger.warning(f"CognitiveCycle recovering from: {error}")
        self.world_model.confidence *= 0.8
