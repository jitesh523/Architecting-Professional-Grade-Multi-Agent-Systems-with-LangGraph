from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from .graph import compile_graph
from langchain_core.messages import HumanMessage
import json
import os
from contextlib import asynccontextmanager
import uvicorn

# Global graph variable
graph = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize checkpointer and graph
    global graph
    async with AsyncSqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
        graph = compile_graph(checkpointer=checkpointer)
        yield
    # Shutdown: Cleanup if needed

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if graph is None:
        return {"error": "Graph not initialized"}

    config = {"configurable": {"thread_id": request.thread_id}}
    inputs = {"messages": [HumanMessage(content=request.message)]}

    async def event_stream():
        try:
            async for event in graph.astream(inputs, config=config):
                # Yield events as SSE
                yield f"data: {json.dumps(str(event))}\n\n"
        except Exception as e:
             yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
