import asyncio
import os
from jarvis.core.kernel import RuntimeKernel
from jarvis.persistence.memory_store import MemoryStore

async def test_persistence_recovery():
    # 1. Start a task and save state
    kernel = RuntimeKernel()
    await kernel.start("Testing recovery", "session_crash_test")

    # Simulate a crash by just creating a new kernel and loading the DB
    print("Simulating process crash...")

    # 2. Restart and Restore
    kernel_new = RuntimeKernel()
    # Check if goal is in DB
    cursor = kernel_new.store.conn.cursor()
    cursor.execute("SELECT goal FROM episodes WHERE id LIKE '%Task_0%'")
    row = cursor.fetchone()
    if row:
        print(f"Goal recovered from DB: {row[0]}")
    else:
        print("Recovery failed: No episodes found.")

if __name__ == "__main__":
    asyncio.run(test_persistence_recovery())
