from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable


State = dict[str, object]
Node = Callable[[State], State]
Condition = Callable[[State], str]


@dataclass
class GraphTrace:
    events: list[dict[str, object]] = field(default_factory=list)

    def add(self, node: str, state: State) -> None:
        self.events.append({"node": node, "state": dict(state)})

    def write(self, path: Path) -> None:
        path.write_text(
            json.dumps({"events": self.events}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


@dataclass
class MiniStateGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: dict[str, str] = field(default_factory=dict)
    conditional_edges: dict[str, tuple[Condition, dict[str, str]]] = field(default_factory=dict)
    entry_point: str = ""

    def add_node(self, name: str, node: Node) -> None:
        self.nodes[name] = node

    def add_edge(self, source: str, target: str) -> None:
        self.edges[source] = target

    def add_conditional_edges(
        self,
        source: str,
        condition: Condition,
        mapping: dict[str, str],
    ) -> None:
        self.conditional_edges[source] = (condition, mapping)

    def set_entry_point(self, name: str) -> None:
        self.entry_point = name

    def invoke(self, state: State, trace: GraphTrace | None = None) -> State:
        current = self.entry_point
        working = dict(state)
        while current != "END":
            if current not in self.nodes:
                raise KeyError(f"Unknown graph node: {current}")
            working = self.nodes[current](working)
            if trace:
                trace.add(current, working)
            if current in self.conditional_edges:
                condition, mapping = self.conditional_edges[current]
                current = mapping[condition(working)]
            else:
                current = self.edges.get(current, "END")
        return working


def build_demo_graph() -> MiniStateGraph:
    graph = MiniStateGraph()

    def call_model(state: State) -> State:
        messages = list(state.get("messages", []))
        messages.append("model: 需要调用 calculator 工具")
        return {**state, "messages": messages, "next": "tool"}

    def call_tool(state: State) -> State:
        messages = list(state.get("messages", []))
        messages.append("tool: calculator 返回 48.0")
        return {**state, "messages": messages, "tool_result": "48.0", "next": "final"}

    def finalize(state: State) -> State:
        messages = list(state.get("messages", []))
        messages.append("final: 根据工具结果生成最终回答")
        return {**state, "messages": messages, "answer": "预算结果是 48.0"}

    def route(state: State) -> str:
        return str(state.get("next", "final"))

    graph.add_node("call_model", call_model)
    graph.add_node("call_tool", call_tool)
    graph.add_node("finalize", finalize)
    graph.set_entry_point("call_model")
    graph.add_conditional_edges(
        "call_model",
        route,
        {
            "tool": "call_tool",
            "final": "finalize",
        },
    )
    graph.add_edge("call_tool", "finalize")
    graph.add_edge("finalize", "END")
    return graph

