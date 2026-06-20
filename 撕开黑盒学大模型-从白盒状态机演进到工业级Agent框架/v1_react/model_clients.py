from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol


class ModelClient(Protocol):
    def complete(self, transcript: str) -> str:
        ...


@dataclass
class ScriptedModel:
    """Deterministic model double used to expose the Agent state machine."""

    steps: list[str] = field(
        default_factory=lambda: [
            "Thought: 先计算预算。\nAction: calculator[128 / 4 + 16]",
            "Thought: 数值已得到，再查询目的地天气。\nAction: weather[杭州]",
            "Thought: 工具信息足够。\nFinal: 预算结果是 48.0，杭州小雨，出门建议带伞。",
        ]
    )
    index: int = 0

    def complete(self, transcript: str) -> str:
        if self.index >= len(self.steps):
            return "Final: 没有更多步骤。"
        output = self.steps[self.index]
        self.index += 1
        return output


@dataclass
class OpenAICompatibleModel:
    """Small HTTP adapter for OpenAI-compatible chat completion endpoints.

    This adapter is intentionally optional. The default demo uses ScriptedModel
    so the core loop is runnable without API keys.
    """

    model: str
    api_key_env: str = "OPENAI_API_KEY"
    base_url: str = "https://api.openai.com/v1/chat/completions"
    temperature: float = 0.0

    def complete(self, transcript: str) -> str:
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing environment variable: {self.api_key_env}")

        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": "Return ReAct text only."},
                {"role": "user", "content": transcript},
            ],
        }
        request = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

