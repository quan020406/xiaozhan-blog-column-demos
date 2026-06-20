from __future__ import annotations

from pathlib import Path

from handmade_graph import GraphTrace, build_demo_graph


def main() -> None:
    trace = GraphTrace()
    graph = build_demo_graph()
    result = graph.invoke({"messages": ["user: 计算预算"]}, trace=trace)
    print(result["answer"])
    trace.write(Path(__file__).with_name("trace.json"))
    print("trace written: trace.json")


if __name__ == "__main__":
    main()

