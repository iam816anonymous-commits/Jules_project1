from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
from jarvis.core.kernel import RuntimeKernel

app = FastAPI(title="Jarvis OS API")
kernel = RuntimeKernel()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return {"response": f"Received: {request.message}"}

@app.post("/api/runtime/start")
async def start_runtime(goal: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(kernel.start, goal, "session_123")
    return {"status": "started", "session_id": "session_123"}

@app.get("/api/runtime/status")
async def get_status():
    return {
        "active": kernel.active,
        "world_state": kernel.cognitive_cycle.world_model.snapshot()
    }

@app.get("/api/memory/summary")
async def get_memory_summary():
    return kernel.store.summarize()

@app.get("/api/memory/episodes")
async def get_episodes():
    """
    Returns actual episodes from MemoryStore.
    """
    cursor = kernel.store.conn.cursor()
    cursor.execute("SELECT * FROM episodes ORDER BY timestamp DESC LIMIT 20")
    rows = cursor.fetchall()
    episodes = []
    for r in rows:
        episodes.append({
            "id": r[0],
            "goal": r[1],
            "reward": r[5],
            "timestamp": r[6]
        })
    return {"episodes": episodes}

@app.get("/api/memory/beliefs")
async def get_beliefs():
    cursor = kernel.store.conn.cursor()
    cursor.execute("SELECT * FROM beliefs")
    rows = cursor.fetchall()
    return {"beliefs": [{"id": r[0], "confidence": r[2]} for r in rows]}
