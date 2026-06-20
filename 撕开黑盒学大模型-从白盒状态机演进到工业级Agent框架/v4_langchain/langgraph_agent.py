from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    messages: list[str]
    summary_memory: str


def build_langgraph_state_machine():
    """Optional migration placeholder for LangGraph StateGraph."""
    try:
        from langgraph.graph import END, StateGraph
    except ImportError as exc:
        raise RuntimeError("Install LangGraph before running this adapter.") from exc

    def call_model(state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        return {"messages": messages + ["model response placeholder"]}

    graph = StateGraph(AgentState)
    graph.add_node("call_model", call_model)
    graph.set_entry_point("call_model")
    graph.add_edge("call_model", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_langgraph_state_machine()
    print(app.invoke({"messages": ["hello"]}))

