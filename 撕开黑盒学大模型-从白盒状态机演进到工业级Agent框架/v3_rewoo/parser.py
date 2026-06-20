from __future__ import annotations

import re

from planner import PlanStep


PLAN_LINE_RE = re.compile(
    r"^(?P<step_id>E\d+):\s*(?P<tool>\w+)\[(?P<argument>.*)\]\s*$"
)


def parse_plan(text: str) -> list[PlanStep]:
    steps: list[PlanStep] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = PLAN_LINE_RE.match(stripped)
        if not match:
            raise ValueError(f"Invalid plan line: {line!r}")
        steps.append(
            PlanStep(
                step_id=match.group("step_id"),
                tool=match.group("tool"),
                argument=match.group("argument"),
            )
        )
    return steps

