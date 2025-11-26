import pytest
from src.graph import graph

@pytest.mark.asyncio
async def test_graph_execution_flow():
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
    assert any("researcher" in e for e in events)
