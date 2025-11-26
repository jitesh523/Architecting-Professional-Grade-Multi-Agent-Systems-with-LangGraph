import pytest
from src.graph import graph

@pytest.mark.asyncio
async def test_graph_execution():
    # We can't easily mock the entire graph execution without complex setup,
    # but we can verify the graph structure and basic compilation.
    
    assert graph is not None
    
    # Verify nodes exist
    assert "planner" in graph.nodes
    assert "supervisor" in graph.nodes
    assert "research_team" in graph.nodes
    assert "coding_team" in graph.nodes
    assert "critic" in graph.nodes

    # Basic execution test with mocked nodes would be ideal, 
    # but for integration we can try a dry run if we mock the internal nodes.
    # For now, we just verify the graph compiles and has the correct structure.
    
    # Test a simple flow that should trigger the fallback logic (since no keys)
    # and eventually finish.
    inputs = {"messages": ["Please research AI"]}
    
    # Collect all events
    events = []
    async for event in graph.astream(inputs):
        events.append(event)
    
    # Verify that we hit the supervisor and researcher
    # Note: The exact number of steps depends on the graph structure
    assert len(events) > 0
    
    # Check if we reached the end
    # In a real integration test with mocks, we'd assert specific state transitions
    # Here we just ensure it runs without error and produces output
    assert any("supervisor" in e for e in events)
    # The node name is now 'research_team'
    # Note: Depending on how the supervisor routes (randomly or fixed in fallback),
    # it might go to research_team or coding_team.
    # Given the input "Please research AI", the fallback logic in supervisor_node
    # (if LLM is None) checks "research" in last message.
    assert any("research_team" in e for e in events)
