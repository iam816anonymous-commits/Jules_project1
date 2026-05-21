import asyncio
import time
from jarvis.persistence.memory_store import MemoryStore
import uuid

async def simulate_long_run(n_observations: int = 1000):
    store = MemoryStore("endurance_test.db")
    print(f"Starting endurance simulation with {n_observations} observations...")

    start_time = time.time()
    for i in range(n_observations):
        episode = {
            "id": str(uuid.uuid4()),
            "goal": "Test Goal",
            "observation": {"key": "val", "index": i},
            "action": {"type": "noop"},
            "reflection": {"status": "ok"},
            "reward": 1.0
        }
        store.save_episode(episode)
        if i % 100 == 0:
            print(f"Processed {i} episodes...")

    duration = time.time() - start_time
    summary = store.summarize()
    print(f"Simulation complete. Duration: {duration:.2f}s")
    print(f"DB Summary: {summary}")

    # Test compact
    store.compact()
    print("DB compacted.")

if __name__ == "__main__":
    asyncio.run(simulate_long_run(1000)) # Reduced for speed in sandbox
