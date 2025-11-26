from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import supervisor_node, research_node, code_node
from .planner import planner_node
from .critic import critic_node
from .teams.research_team import research_team_graph
from .teams.coding_team import coding_team_graph

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("research_team", research_team_graph)
workflow.add_node("coding_team", coding_team_graph)
workflow.add_node("critic", critic_node)

# Define edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "supervisor")

# Conditional edges from supervisor
workflow.add_conditional_edges(
    "supervisor",
    lambda x: x["next_step"],
    {
        "researcher": "research_team", # Route to team
        "coder": "coding_team",       # Route to team
        "FINISH": "critic"
    }
)

# Edges from teams back to supervisor
workflow.add_edge("research_team", "supervisor")
workflow.add_edge("coding_team", "supervisor")

# Conditional edges from critic
workflow.add_conditional_edges(
    "critic",
    lambda x: x["next_step"],
    {
        "supervisor": "supervisor",
        "FINISH": END
    }
)


# Compile
graph = workflow.compile()

def compile_graph(checkpointer=None):
    return workflow.compile(checkpointer=checkpointer)
