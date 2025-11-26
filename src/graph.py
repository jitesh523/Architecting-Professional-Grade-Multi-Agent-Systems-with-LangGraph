from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import supervisor_node, research_node, code_node

def route_supervisor(state: AgentState):
    next_step = state.get("next_step")
    if next_step == "researcher":
        return "researcher"
    elif next_step == "coder":
        return "coder"
    else:
        return END

workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("researcher", research_node)
workflow.add_node("coder", code_node)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "researcher": "researcher",
        "coder": "coder",
        "FINISH": END,
        END: END
    }
)

# Add edges from workers back to supervisor
# In a more complex graph, we might route to a "retry" node if error_count > 0
workflow.add_edge("researcher", "supervisor")
workflow.add_edge("coder", "supervisor")

graph = workflow.compile()
