from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import graph
from src.state import AgentState
import uvicorn

app = FastAPI(title="LangGraph Agent API")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Run the graph with the user's message and return the final state.
    """
    try:
        inputs = {"messages": [request.message]}
        # For simplicity in this prototype, we await the final result
        # In production, you might want to stream events using Server-Sent Events (SSE)
        final_state = await graph.ainvoke(inputs)
        
        # Extract the last message
        messages = final_state.get("messages", [])
        last_message = messages[-1] if messages else "No response"
        
        return {
            "response": str(last_message),
            "full_state": final_state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
