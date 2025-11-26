from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from .state import AgentState
import os

# Initialize LLM
try:
    llm = ChatOpenAI(model="gpt-4o")
except Exception:
    llm = None

class Plan(BaseModel):
    """Plan to follow for the user request."""
    steps: List[str] = Field(description="List of steps to follow, in order.")

def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Planner node that decomposes the user request into steps.
    """
    messages = state['messages']
    
    if not llm:
        # Fallback for testing
        return {"plan": ["Research the topic", "Write code"]}

    system_prompt = (
        "You are a planner agent. Your job is to break down the user's request into a clear, step-by-step plan.\n"
        "The available workers are: Researcher, Coder.\n"
        "Ensure the plan utilizes these workers effectively.\n"
        "Return a list of steps."
    )
    
    # Convert string messages to HumanMessage if needed
    # Assuming messages are strings based on current state definition
    input_messages = [SystemMessage(content=system_prompt)]
    for m in messages:
        if isinstance(m, str):
            input_messages.append(HumanMessage(content=m))
        else:
            input_messages.append(m)

    try:
        structured_llm = llm.with_structured_output(Plan)
        plan_result = structured_llm.invoke(input_messages)
        return {"plan": plan_result.steps}
    except Exception as e:
        print(f"Planner Error: {e}")
        return {"plan": ["Error generating plan", "Proceed with caution"]}
