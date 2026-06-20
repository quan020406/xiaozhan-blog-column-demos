from __future__ import annotations

import re
from dataclasses import dataclass

from model_clients import ModelClient
from trace_recorder import TraceRecorder
from tools import ToolRegistry, registry


ACTION_RE = re.compile(r"^Action:\s*(?P<name>\w+)\[(?P<arg>.*)\]\s*$")


@dataclass
class ReactAgent:
    model: ModelClient
    tools: ToolRegistry = registry
    max_steps: int = 8
    trace: TraceRecorder | None = None

    def run(self, task: str) -> str:
        transcript = self._build_prompt(task)
        if self.trace:
            self.trace.add(0, "prompt", text=transcript)
        for step in range(1, self.max_steps + 1):
            output = self.model.complete(transcript)
            print(f"\n[step {step}] model\n{output}")
            if self.trace:
                self.trace.add(step, "model_output", text=output)

            final_line = next(
                (line for line in output.splitlines() if line.startswith("Final:")),
                "",
            )
            if final_line:
                answer = final_line.removeprefix("Final:").strip()
                if self.trace:
                    self.trace.add(step, "final", answer=answer)
                return answer

            action_line = next(
                (line for line in output.splitlines() if line.startswith("Action:")),
                "",
            )
            match = ACTION_RE.match(action_line)
            if not match:
                if self.trace:
                    self.trace.add(step, "parse_error", action_line=action_line, output=output)
                raise ValueError(f"Cannot parse action line: {action_line!r}")

            tool_name = match.group("name")
            tool_arg = match.group("arg")
            if self.trace:
                self.trace.add(step, "tool_call", name=tool_name, argument=tool_arg)
            observation = self.tools.call(tool_name, tool_arg)
            print(f"[step {step}] observation\n{observation}")
            if self.trace:
                self.trace.add(step, "observation", text=str(observation))
            transcript += f"\n{output}\nObservation: {observation}"

        raise TimeoutError("Agent exceeded max_steps.")

    def _build_prompt(self, task: str) -> str:
        tool_lines = [
            f"- {spec.name}({spec.parameters}): {spec.description}"
            for spec in self.tools.schema()
        ]
        return (
            "You are a deterministic ReAct agent. Use Thought, Action, Observation, Final.\n"
            "Available tools:\n"
            + "\n".join(tool_lines)
            + f"\nTask: {task}"
        )
