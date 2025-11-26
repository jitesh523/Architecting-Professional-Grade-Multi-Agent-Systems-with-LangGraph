import pytest
from unittest.mock import MagicMock, patch
from src.critic import critic_node, Critique
from src.state import AgentState

@patch("src.critic.llm")
def test_critic_node_approve(mock_llm):
    # Mock state
    mock_state = AgentState(messages=["User: Build a weather app", "Coder: Here is the code"], next_step=None, error_count=0, plan=[], critique=None)
    
    # Mock LLM response for approval
    mock_critique = Critique(approved=True, feedback="Good job")
    mock_llm.with_structured_output.return_value.invoke.return_value = mock_critique
    
    result = critic_node(mock_state)
    
    assert result["next_step"] == "FINISH"
    assert result["critique"] == "Good job"

@patch("src.critic.llm")
def test_critic_node_reject(mock_llm):
    # Mock state
    mock_state = AgentState(messages=["User: Build a weather app", "Coder: Here is the code"], next_step=None, error_count=0, plan=[], critique=None)
    
    # Mock LLM response for rejection
    mock_critique = Critique(approved=False, feedback="Missing error handling")
    mock_llm.with_structured_output.return_value.invoke.return_value = mock_critique
    
    result = critic_node(mock_state)
    
    assert result["next_step"] == "supervisor"
    assert result["critique"] == "Missing error handling"
    assert "messages" in result
    assert "Critic: Missing error handling" in result["messages"][0]

@patch("src.critic.llm", None)
def test_critic_node_fallback():
    # Test fallback when LLM is None
    mock_state = AgentState(messages=["User: Build a weather app"], next_step=None, error_count=0, plan=[], critique=None)
    
    result = critic_node(mock_state)
    
    assert result["next_step"] == "FINISH"
