import pytest
from unittest.mock import MagicMock, patch
from src.planner import planner_node, Plan
from src.state import AgentState

@patch("src.planner.llm")
def test_planner_node(mock_llm):
    # Mock state
    mock_state = AgentState(messages=["User: Build a weather app"], next_step=None, error_count=0, plan=[])
    
    # Mock LLM response
    mock_plan = Plan(steps=["Research weather APIs", "Write python code"])
    mock_llm.with_structured_output.return_value.invoke.return_value = mock_plan
    
    result = planner_node(mock_state)
    
    assert "plan" in result
    assert result["plan"] == ["Research weather APIs", "Write python code"]
    assert len(result["plan"]) == 2

@patch("src.planner.llm", None)
def test_planner_node_fallback():
    # Test fallback when LLM is None
    mock_state = AgentState(messages=["User: Build a weather app"], next_step=None, error_count=0, plan=[])
    
    result = planner_node(mock_state)
    
    assert "plan" in result
    assert len(result["plan"]) > 0
