from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanStep:
    step_id: str
    tool: str
    argument: str


def build_plan(task: str) -> list[PlanStep]:
    return [
        PlanStep("E1", "fetch_price", "GPU"),
        PlanStep("E2", "fetch_weather", "杭州"),
        PlanStep("E3", "unstable_inventory", "GPU"),
        PlanStep("E4", "summarize", "结合 #E1、#E2、#E3 给出出门采购建议"),
    ]


def build_plan_text(task: str) -> str:
    return "\n".join(
        [
            "E1: fetch_price[GPU]",
            "E2: fetch_weather[杭州]",
            "E3: unstable_inventory[GPU]",
            "E4: summarize[结合 #E1、#E2、#E3 给出出门采购建议]",
        ]
    )
