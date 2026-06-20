from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, str]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self._tools[func.__name__] = func
        return func

    def schema(self) -> list[ToolSpec]:
        specs: list[ToolSpec] = []
        for name, func in self._tools.items():
            signature = inspect.signature(func)
            parameters = {
                param_name: str(param.annotation)
                for param_name, param in signature.parameters.items()
            }
            specs.append(
                ToolSpec(
                    name=name,
                    description=(inspect.getdoc(func) or "").splitlines()[0],
                    parameters=parameters,
                )
            )
        return specs

    def call(self, name: str, raw_arg: str) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        func = self._tools[name]
        signature = inspect.signature(func)
        if len(signature.parameters) != 1:
            raise ValueError("This demo runtime only supports one-argument tools.")
        return func(raw_arg)


registry = ToolRegistry()


@registry.register
def calculator(expression: str) -> str:
    """Evaluate a small arithmetic expression."""
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        raise ValueError("Expression contains unsupported characters.")
    return str(eval(expression, {"__builtins__": {}}, {}))


@registry.register
def weather(city: str) -> str:
    """Return a deterministic weather report for a city."""
    reports = {
        "杭州": "小雨，气温 23 度，建议带伞。",
        "上海": "多云，气温 25 度，适合短途出门。",
    }
    return reports.get(city.strip(), "天气未知，建议查询可靠来源。")

