"""Unit tests for the StateGraph orchestrator."""

import asyncio
import pytest

from cloudoptima.graph import StateGraph

@pytest.mark.asyncio
async def test_simple_sequential_execution():
    """Ensure sequential execution modifies state correctly."""
    graph = StateGraph()
    
    async def node_a(state: dict[str, list[str]]) -> None:
        state["history"].append("A")
        
    async def node_b(state: dict[str, list[str]]) -> None:
        state["history"].append("B")

    graph.add_node("A", node_a)
    graph.add_node("B", node_b)
    graph.add_edge("A", "B")
    graph.set_entry_point("A")
    
    state = {"history": []}
    result = await graph.run(state)
    assert result["history"] == ["A", "B"]


@pytest.mark.asyncio
async def test_parallel_execution():
    """Ensure list of nodes are executed concurrently (fan-out)."""
    graph = StateGraph()
    
    async def parallel_a(state: dict[str, list[str]]) -> None:
        await asyncio.sleep(0.01)
        state["history"].append("A")
        
    async def parallel_b(state: dict[str, list[str]]) -> None:
        state["history"].append("B")

    # B will finish before A because A sleeps
    graph.add_node("parallel_group", [parallel_a, parallel_b])
    graph.set_entry_point("parallel_group")
    
    state = {"history": []}
    result = await graph.run(state)
    # The order can be [B, A] due to sleep in A
    assert len(result["history"]) == 2
    assert set(result["history"]) == {"A", "B"}


@pytest.mark.asyncio
async def test_max_steps_halts_execution(caplog):
    """Ensure the graph terminates safely when max_steps is exceeded."""
    graph = StateGraph()
    
    async def node_loop(state: dict[str, int]) -> None:
        state["count"] += 1

    graph.add_node("Loop", node_loop)
    graph.add_edge("Loop", "Loop")
    graph.set_entry_point("Loop")
    
    state = {"count": 0}
    result = await graph.run(state, max_steps=5)
    
    assert result["count"] == 5
    assert "max_steps reached" in caplog.text


@pytest.mark.asyncio
async def test_exception_bubbles_up():
    """Ensure exceptions inside nodes fail the graph explicitly."""
    graph = StateGraph()
    
    async def faulty_node(state: dict) -> None:
        raise ValueError("Intentional crash")

    graph.add_node("Fault", faulty_node)
    graph.set_entry_point("Fault")
    
    state = {}
    with pytest.raises(ValueError, match="Intentional crash"):
        await graph.run(state)


@pytest.mark.asyncio
async def test_missing_entry_point_raises_error():
    """Ensure the graph validates existence of an entry point."""
    graph = StateGraph()
    
    with pytest.raises(ValueError, match="requires an entry point"):
        await graph.run({})
