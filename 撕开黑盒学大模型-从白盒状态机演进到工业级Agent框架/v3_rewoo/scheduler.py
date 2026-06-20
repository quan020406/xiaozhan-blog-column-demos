from __future__ import annotations

import asyncio
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from planner import PlanStep
from worker import TOOLS


DEPENDENCY_RE = re.compile(r"#(?P<step_id>E\d+)")


@dataclass
class TimelineEvent:
    runner: str
    step_id: str
    event: str
    timestamp: float
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionTrace:
    started_at: float = field(default_factory=time.perf_counter)
    events: list[TimelineEvent] = field(default_factory=list)

    def add(self, runner: str, step_id: str, event: str, **payload: Any) -> None:
        self.events.append(
            TimelineEvent(
                runner=runner,
                step_id=step_id,
                event=event,
                timestamp=round(time.perf_counter() - self.started_at, 4),
                payload=payload,
            )
        )

    def to_dict(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self.events]


def dependencies(step: PlanStep) -> set[str]:
    return set(DEPENDENCY_RE.findall(step.argument))


def resolve_argument(argument: str, results: dict[str, str]) -> str:
    for step_id, value in results.items():
        argument = argument.replace(f"#{step_id}", value)
    return argument


async def call_tool(step: PlanStep, argument: str, timeout: float) -> str:
    return await asyncio.wait_for(TOOLS[step.tool](argument), timeout=timeout)


async def run_parallel(
    plan: list[PlanStep],
    trace: ExecutionTrace | None = None,
    timeout: float = 0.6,
) -> dict[str, str]:
    pending = {step.step_id: step for step in plan}
    results: dict[str, str] = {}
    while pending:
        ready = [
            step
            for step in pending.values()
            if dependencies(step).issubset(results)
        ]
        if not ready:
            raise RuntimeError("Plan has unresolved or circular dependencies.")

        async def run_step(step: PlanStep) -> tuple[str, str]:
            try:
                arg = resolve_argument(step.argument, results)
                if trace:
                    trace.add("parallel", step.step_id, "start", tool=step.tool, argument=arg)
                value = await call_tool(step, arg, timeout)
                if trace:
                    trace.add("parallel", step.step_id, "success", value=value)
                return step.step_id, value
            except asyncio.TimeoutError:
                value = f"ERROR: {step.tool} timed out after {timeout}s"
                if trace:
                    trace.add("parallel", step.step_id, "timeout", value=value)
                return step.step_id, value
            except Exception as exc:  # noqa: BLE001 - demo keeps failures as observations.
                value = f"ERROR: {exc}"
                if trace:
                    trace.add("parallel", step.step_id, "error", value=value)
                return step.step_id, value

        completed = await asyncio.gather(*(run_step(step) for step in ready))
        for step_id, value in completed:
            results[step_id] = value
            pending.pop(step_id)
    return results


async def run_serial(
    plan: list[PlanStep],
    trace: ExecutionTrace | None = None,
    timeout: float = 0.6,
) -> dict[str, str]:
    results: dict[str, str] = {}
    for step in plan:
        arg = resolve_argument(step.argument, results)
        try:
            if trace:
                trace.add("serial", step.step_id, "start", tool=step.tool, argument=arg)
            results[step.step_id] = await call_tool(step, arg, timeout)
            if trace:
                trace.add("serial", step.step_id, "success", value=results[step.step_id])
        except asyncio.TimeoutError:
            results[step.step_id] = f"ERROR: {step.tool} timed out after {timeout}s"
            if trace:
                trace.add("serial", step.step_id, "timeout", value=results[step.step_id])
        except Exception as exc:  # noqa: BLE001
            results[step.step_id] = f"ERROR: {exc}"
            if trace:
                trace.add("serial", step.step_id, "error", value=results[step.step_id])
    return results
