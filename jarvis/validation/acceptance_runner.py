import asyncio
import logging
from jarvis.core.kernel import RuntimeKernel
from jarvis.persistence.memory_store import MemoryStore

async def run_acceptance_scenario():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("AcceptanceRunner")

    # 1. Initialize
    kernel = RuntimeKernel()
    goal = "Research Python async docs, extract notes, and save to notes.txt"

    logger.info(f"Starting Acceptance Gate Scenario: {goal}")

    # 2. Start (Session will automatically decompose and orchestrate)
    # We run in a task so we can monitor or interrupt if needed
    kernel_task = asyncio.create_task(kernel.start(goal, "acceptance_v1_001"))

    # 3. Monitor execution progress for 30s (simulated duration for headless env)
    await asyncio.sleep(10)

    # 4. Cleanup
    await kernel.stop()
    logger.info("Scenario run complete. Analyzing database...")

    # 5. Verify Database Artifacts
    store = MemoryStore()
    summary = store.summarize()
    print(f"Artifacts collected: {summary['episode_count']} episodes in database.")

    # Query last 5 actions
    cursor = store.Session().connection().connection.cursor()
    cursor.execute("SELECT goal, action, timestamp FROM episodes ORDER BY timestamp DESC LIMIT 5")
    actions = cursor.fetchall()
    for goal, action, ts in actions:
        print(f"[{ts}] Goal: {goal} -> Action: {action}")

if __name__ == "__main__":
    asyncio.run(run_acceptance_scenario())
