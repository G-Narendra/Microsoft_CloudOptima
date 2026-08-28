"""State Graph for agent workflow orchestration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

_logger = logging.getLogger(__name__)


class StateGraph:
    """A Directed Acyclic Graph (DAG) for orchestrating state transitions.
    
    Nodes can be async functions, or a list of async functions to run
    in parallel.
    """

    def __init__(self) -> None:
        self.nodes: dict[str, Callable | list[Callable]] = {}
        self.edges: dict[str, str] = {}
        self.entry_point: str | None = None

    def add_node(self, name: str, action: Callable | list[Callable]) -> None:
        """Register a node in the graph."""
        self.nodes[name] = action

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Define a transition from one node to the next."""
        self.edges[from_node] = to_node

    def set_entry_point(self, name: str) -> None:
        """Set the starting node."""
        self.entry_point = name

    async def run(self, state: Any, max_steps: int = 15) -> Any:
        """Execute the graph until completion or max_steps is reached."""
        if not self.entry_point:
            raise ValueError("StateGraph requires an entry point")

        current_node = self.entry_point
        steps = 0

        while current_node and steps < max_steps:
            action = self.nodes.get(current_node)
            if not action:
                break

            _logger.info("Graph running node: %s", current_node)

            try:
                if isinstance(action, list):
                    await asyncio.gather(*(a(state) for a in action))
                else:
                    await action(state)
            except Exception as exc:
                _logger.exception("Graph execution failed at node %s", current_node)
                raise exc

            current_node = self.edges.get(current_node)
            steps += 1

        if steps >= max_steps:
            _logger.warning("Graph execution aborted: max_steps reached")

        return state
