from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
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
    return {"active": kernel.active, "world_state": kernel.world_model.snapshot()}

@app.get("/api/memory")
async def get_memory():
    return {"episodes": [], "semantic": []}
