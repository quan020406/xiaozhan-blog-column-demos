from __future__ import annotations

from dataclasses import dataclass

from memory_manager import MemoryManager, Message


@dataclass
class MemoryAwareAgent:
    memory: MemoryManager

    def chat(self, user_input: str, user_id: str = "default") -> str:
        context = self.memory.build_context(user_input, user_id=user_id)
        answer = self._deterministic_answer(user_input, context)
        self.memory.add(Message(role="user", content=user_input, user_id=user_id))
        self.memory.add(Message(role="assistant", content=answer, user_id=user_id))
        return answer

    def _deterministic_answer(self, user_input: str, context: str) -> str:
        if "记忆污染" in user_input:
            return "先做阈值过滤，再把短期窗口、摘要记忆和长期检索分层处理。"
        if context:
            return "我会基于当前会话窗口和通过阈值筛选的历史记忆回答。"
        return "当前没有可用历史上下文，先按本轮输入回答。"

