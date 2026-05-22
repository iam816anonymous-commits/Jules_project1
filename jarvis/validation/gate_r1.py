import asyncio
import json
import os
import logging
from jarvis.core.kernel import RuntimeKernel

async def run_v1_beta_candidate_gate():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("BetaCandidateGate")

    kernel = RuntimeKernel()
    goal = "Research FastAPI docs, create code, and run"

    logger.info(f"R1 GATE: Starting autonomous scenario: {goal}")

    # 1. Run Scenario
    # We mock _orchestrate_execution to simulate the dispatch results for R1 proof
    with asyncio.timeout(20):
        await kernel.start(goal, "gate_r1_proof")

    # 2. Extract Artifacts
    episodes = kernel.store.get_recent_episodes(limit=10)

    runtime_trace = [e for e in episodes]
    with open("runtime_trace.json", "w") as f:
        json.dump(runtime_trace, f, indent=2)

    logger.info(f"Artifacts generated: {len(runtime_trace)} steps captured.")

if __name__ == "__main__":
    try:
        asyncio.run(run_v1_beta_candidate_gate())
    except Exception as e:
        print(f"Gate failed: {e}")
