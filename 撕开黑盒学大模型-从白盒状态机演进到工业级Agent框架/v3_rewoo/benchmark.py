from __future__ import annotations

import asyncio
import json
import time
from dataclasses import asdict
from pathlib import Path

from parser import parse_plan
from planner import build_plan_text
from scheduler import ExecutionTrace, run_parallel, run_serial


ROOT = Path(__file__).resolve().parent


async def measure(label: str, runner, plan, trace: ExecutionTrace) -> dict:
    started = time.perf_counter()
    results = await runner(plan, trace=trace)
    elapsed = time.perf_counter() - started
    print(f"{label}: {elapsed:.3f}s")
    for step_id, value in results.items():
        print(f"  {step_id}: {value}")
    return {
        "label": label,
        "elapsed": round(elapsed, 3),
        "results": results,
    }


async def main() -> None:
    plan_text = build_plan_text("采购前做价格和天气判断")
    plan = parse_plan(plan_text)
    print("plan:")
    print(plan_text)
    trace = ExecutionTrace()
    serial = await measure("serial ReAct-like execution", run_serial, plan, trace)
    parallel = await measure("parallel ReWOO-like execution", run_parallel, plan, trace)
    payload = {
        "plan_text": plan_text,
        "plan": [asdict(step) for step in plan],
        "runs": [serial, parallel],
        "timeline": trace.to_dict(),
    }
    (ROOT / "trace.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("trace written: trace.json")


if __name__ == "__main__":
    asyncio.run(main())
