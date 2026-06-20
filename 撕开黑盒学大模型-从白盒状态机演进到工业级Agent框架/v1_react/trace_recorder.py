from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TraceEvent:
    step: int
    phase: str
    payload: dict[str, Any]


@dataclass
class TraceRecorder:
    events: list[TraceEvent] = field(default_factory=list)

    def add(self, step: int, phase: str, **payload: Any) -> None:
        self.events.append(TraceEvent(step=step, phase=phase, payload=payload))

    def write(self, path: Path) -> None:
        path.write_text(
            json.dumps([asdict(event) for event in self.events], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

