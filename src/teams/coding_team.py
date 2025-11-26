from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from ..state import AgentState
from ..nodes import code_node # Reuse the existing coder node

def coding_supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Supervisor for the coding team.
    """
    messages = state['messages']
    last_message = messages[-1] if messages else ""
    
    # Simple logic: If the last message is a result from the coder, we are done.
    if isinstance(last_message, str):
        content = last_message
    else:
        content = last_message.content

    if "Coder" in content:
         return {"next_step": "FINISH"}
    
    return {"next_step": "coding_worker"}

# Define the coding team graph
coding_builder = StateGraph(AgentState)

coding_builder.add_node("coding_supervisor", coding_supervisor_node)
coding_builder.add_node("coding_worker", code_node)

coding_builder.set_entry_point("coding_supervisor")

coding_builder.add_conditional_edges(
    "coding_supervisor",
    lambda x: x["next_step"],
    {
        "coding_worker": "coding_worker",
        "FINISH": END
    }
)

coding_builder.add_edge("coding_worker", "coding_supervisor")

coding_team_graph = coding_builder.compile()
