import pytest
from src.teams.research_team import research_supervisor_node
from src.teams.coding_team import coding_supervisor_node
from src.state import AgentState
from langchain_core.messages import HumanMessage

def test_research_supervisor_routing():
    # Test routing to worker
    state = AgentState(messages=["User: Research AI"], next_step=None, error_count=0, plan=[], critique=None)
    result = research_supervisor_node(state)
    assert result["next_step"] == "research_worker"

    # Test routing to FINISH
    state = AgentState(messages=["User: Research AI", HumanMessage(content="Researcher: Found info")], next_step=None, error_count=0, plan=[], critique=None)
    result = research_supervisor_node(state)
    assert result["next_step"] == "FINISH"

def test_coding_supervisor_routing():
    # Test routing to worker
    state = AgentState(messages=["User: Write code"], next_step=None, error_count=0, plan=[], critique=None)
    result = coding_supervisor_node(state)
    assert result["next_step"] == "coding_worker"

    # Test routing to FINISH
    state = AgentState(messages=["User: Write code", HumanMessage(content="Coder: Here is code")], next_step=None, error_count=0, plan=[], critique=None)
    result = coding_supervisor_node(state)
    assert result["next_step"] == "FINISH"
