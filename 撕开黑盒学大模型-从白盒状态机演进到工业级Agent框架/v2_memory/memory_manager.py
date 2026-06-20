from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from vector_store import JsonVectorStore, VectorRecord


@dataclass(frozen=True)
class Message:
    role: str
    content: str
    user_id: str = "default"


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in text.replace("，", " ").replace("。", " ").split()]


def cosine_similarity(left: str, right: str) -> float:
    left_counts = Counter(tokenize(left))
    right_counts = Counter(tokenize(right))
    if not left_counts or not right_counts:
        return 0.0
    shared = set(left_counts) & set(right_counts)
    numerator = sum(left_counts[token] * right_counts[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return numerator / (left_norm * right_norm)


@dataclass
class MemoryManager:
    window_size: int = 4
    threshold: float = 0.2
    store_path: Path = Path("memory_store.json")
    recent_messages: list[Message] = field(default_factory=list)
    summary_memory: str = ""
    vector_store: JsonVectorStore = field(init=False)

    def __post_init__(self) -> None:
        self.vector_store = JsonVectorStore(self.store_path)

    def add(self, message: Message) -> None:
        self.recent_messages.append(message)
        self.vector_store.add(message.user_id, message.role, message.content)
        if len(self.recent_messages) > self.window_size:
            expired = self.recent_messages.pop(0)
            self.summary_memory = self._summarize(expired)

    def retrieve(self, query: str, user_id: str = "default", top_k: int = 3) -> list[tuple[float, VectorRecord]]:
        return self.vector_store.search(query, user_id=user_id, top_k=top_k, threshold=self.threshold)

    def retrieve_without_threshold(
        self,
        query: str,
        user_id: str = "default",
        top_k: int = 3,
    ) -> list[tuple[float, VectorRecord]]:
        return self.vector_store.search(query, user_id=user_id, top_k=top_k, threshold=None)

    def erase_user(self, user_id: str) -> None:
        self.recent_messages = [message for message in self.recent_messages if message.user_id != user_id]
        self.vector_store.erase_user(user_id)

    def build_context(self, query: str, user_id: str = "default") -> str:
        retrieved = self.retrieve(query, user_id=user_id)
        parts = []
        if self.summary_memory:
            parts.append(f"summary_memory: {self.summary_memory}")
        parts.extend(
            f"recent: {message.role}: {message.content}"
            for message in self.recent_messages
            if message.user_id == user_id
        )
        parts.extend(
            f"retrieved({score:.2f}): {record.content}"
            for score, record in retrieved
        )
        return "\n".join(parts)

    def _summarize(self, expired: Message) -> str:
        prefix = f"{self.summary_memory} " if self.summary_memory else ""
        return (prefix + f"{expired.role} 曾提到：{expired.content}").strip()
