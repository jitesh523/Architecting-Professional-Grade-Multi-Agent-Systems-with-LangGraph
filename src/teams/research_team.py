from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from ..state import AgentState
from ..nodes import research_node # Reuse the existing researcher node

# Initialize LLM
try:
    llm = ChatOpenAI(model="gpt-4o")
except Exception:
    llm = None

def research_supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Supervisor for the research team.
    """
    messages = state['messages']
    last_message = messages[-1] if messages else ""
    
    # Simple logic: If the last message is a result from the researcher, we are done.
    # In a real system, this supervisor would evaluate if more research is needed.
    # Simple logic: If the last message is a result from the researcher, we are done.
    if isinstance(last_message, str):
        content = last_message
    else:
        content = last_message.content
        
    if "Researcher" in content:
         return {"next_step": "FINISH"}
    
    # Otherwise, instruct the researcher
    return {"next_step": "research_worker"}

# Define the research team graph
research_builder = StateGraph(AgentState)

research_builder.add_node("research_supervisor", research_supervisor_node)
research_builder.add_node("research_worker", research_node)

research_builder.set_entry_point("research_supervisor")

research_builder.add_conditional_edges(
    "research_supervisor",
    lambda x: x["next_step"],
    {
        "research_worker": "research_worker",
        "FINISH": END
    }
)

research_builder.add_edge("research_worker", "research_supervisor")

research_team_graph = research_builder.compile()
