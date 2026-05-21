import asyncio
import logging
from typing import List, Dict, Any
from jarvis.core.kernel import RuntimeKernel

logger = logging.getLogger(__name__)

class ScenarioRunner:
    def __init__(self, kernel: RuntimeKernel):
        self.kernel = kernel

    async def run_scenario(self, name: str, goal: str) -> bool:
        logger.info(f"ScenarioRunner: Starting scenario '{name}' with goal: {goal}")
        try:
            await self.kernel.start(goal, f"scenario_{name}")
            # Monitor until goal is achieved or timeout
            timeout = 300 # 5 minutes
            start_time = asyncio.get_event_loop().time()
            while self.kernel.active:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.error(f"Scenario '{name}' timed out.")
                    await self.kernel.stop()
                    return False
                await asyncio.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Scenario '{name}' failed: {e}")
            return False

    async def run_v1_suite(self):
        scenarios = [
            ("Research", "Research autonomous agents and save a summary to agents.md"),
            ("Coding", "Create a python script that prints fibonacci and run it"),
        ]
        results = {}
        for name, goal in scenarios:
            results[name] = await self.run_scenario(name, goal)
        return results
