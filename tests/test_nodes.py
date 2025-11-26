import pytest
from unittest.mock import MagicMock, patch
from src.nodes import supervisor_node, research_node, code_node
from src.state import AgentState

@pytest.fixture
def mock_state():
    return AgentState(messages=["User: Do some research"], next_step=None, error_count=0)

@patch("src.nodes.llm")
def test_supervisor_node_routing(mock_llm, mock_state):
    # Mock the LLM response for structured output
    mock_llm.with_structured_output.return_value.invoke.return_value = {"next": "researcher"}
    # Mock token counter with a real function
    mock_llm.get_num_tokens_from_messages = lambda messages: 10
    
    result = supervisor_node(mock_state)
    assert result["next_step"] == "researcher"

@patch("src.nodes.llm")
def test_supervisor_node_finish(mock_llm, mock_state):
    mock_llm.with_structured_output.return_value.invoke.return_value = {"next": "FINISH"}
    mock_llm.get_num_tokens_from_messages = lambda messages: 10
    
    result = supervisor_node(mock_state)
    assert result["next_step"] == "FINISH"

@patch("src.nodes.search_tool")
def test_research_node_success(mock_search, mock_state):
    mock_search.invoke.return_value = [{"url": "http://example.com", "content": "AI is cool"}]
    
    result = research_node(mock_state)
    assert "Researcher: Found 1 results" in result["messages"][0]

@patch("src.nodes.llm")
def test_code_node_success(mock_llm, mock_state):
    mock_llm.invoke.return_value.content = "print('Hello World')"
    
    result = code_node(mock_state)
    assert "Coder: print('Hello World')" in result["messages"][0]

def test_supervisor_fallback_logic():
    # Test fallback when LLM is None (simulated by patching or just calling if logic allows)
    # Since we can't easily set the global llm variable to None in the module without reloading,
    # we rely on the logic that checks `if not llm`. 
    # However, for unit testing, we can patch the module variable.
    with patch("src.nodes.llm", None):
        state = AgentState(messages=["User: research AI"], next_step=None, error_count=0)
        result = supervisor_node(state)
        assert result["next_step"] == "researcher"

        state = AgentState(messages=["User: write code"], next_step=None, error_count=0)
        result = supervisor_node(state)
        assert result["next_step"] == "coder"
