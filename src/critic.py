from typing import Dict, Any, Literal
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

class Critique(BaseModel):
    """Critique of the work done."""
    approved: bool = Field(description="Whether the work is satisfactory and complete.")
    feedback: str = Field(description="Feedback on what needs improvement if not approved, or a summary if approved.")

def critic_node(state: AgentState) -> Dict[str, Any]:
    """
    Critic node that reviews the conversation and provides feedback.
    """
    messages = state['messages']
    
    if not llm:
        # Fallback for testing
        return {"critique": "Approved (Mock)", "next_step": "FINISH"}

    system_prompt = (
        "You are a critic agent. Your job is to review the work done by the Researcher and Coder.\n"
        "Check if the user's original request has been fully addressed.\n"
        "If the work is satisfactory, approve it.\n"
        "If there are errors, missing information, or the quality is low, reject it and provide constructive feedback.\n"
    )
    
    # Convert string messages to HumanMessage if needed
    input_messages = [SystemMessage(content=system_prompt)]
    for m in messages:
        if isinstance(m, str):
            input_messages.append(HumanMessage(content=m))
        else:
            input_messages.append(m)

    try:
        structured_llm = llm.with_structured_output(Critique)
        critique_result = structured_llm.invoke(input_messages)
        
        if critique_result.approved:
            return {
                "critique": critique_result.feedback,
                "next_step": "FINISH"
            }
        else:
            return {
                "critique": critique_result.feedback,
                "messages": [f"Critic: {critique_result.feedback}"],
                "next_step": "supervisor" # Route back to supervisor to address feedback
            }
            
    except Exception as e:
        print(f"Critic Error: {e}")
        return {"critique": "Error during critique", "next_step": "FINISH"}
