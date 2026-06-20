from __future__ import annotations

from pathlib import Path

from agent import ReactAgent
from model_clients import ScriptedModel
from trace_recorder import TraceRecorder


def main() -> None:
    task = "计算预算，并根据杭州天气判断是否适合出门。"
    trace = TraceRecorder()
    answer = ReactAgent(model=ScriptedModel(), trace=trace).run(task)
    print(f"\nfinal answer: {answer}")
    trace_path = Path(__file__).with_name("trace.json")
    trace.write(trace_path)
    print(f"trace written: {trace_path.name}")


if __name__ == "__main__":
    main()

