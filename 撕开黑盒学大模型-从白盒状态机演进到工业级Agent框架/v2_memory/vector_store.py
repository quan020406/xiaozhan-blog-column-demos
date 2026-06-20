from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


def tokenize(text: str) -> list[str]:
    normalized = (
        text.lower()
        .replace("，", " ")
        .replace("。", " ")
        .replace("：", " ")
        .replace("/", " ")
    )
    tokens = [token for token in normalized.split() if token]
    cjk_chunks = re.findall(r"[\u4e00-\u9fff]+", text)
    for chunk in cjk_chunks:
        tokens.extend(chunk[index : index + 2] for index in range(max(len(chunk) - 1, 0)))
    return tokens


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


@dataclass(frozen=True)
class VectorRecord:
    record_id: int
    user_id: str
    role: str
    content: str


class JsonVectorStore:
    """Tiny persistent vector-store facade.

    It deliberately uses lexical cosine similarity so the demo stays dependency
    free. The interface mirrors a real vector DB enough to discuss thresholding,
    top-k pollution and user-scoped erasure.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.records: list[VectorRecord] = []
        self._next_id = 1
        self.load()

    def add(self, user_id: str, role: str, content: str) -> VectorRecord:
        record = VectorRecord(self._next_id, user_id, role, content)
        self._next_id += 1
        self.records.append(record)
        self.save()
        return record

    def search(
        self,
        query: str,
        user_id: str,
        top_k: int = 3,
        threshold: float | None = None,
    ) -> list[tuple[float, VectorRecord]]:
        scored = [
            (cosine_similarity(query, record.content), record)
            for record in self.records
            if record.user_id == user_id
        ]
        if threshold is not None:
            scored = [(score, record) for score, record in scored if score >= threshold]
        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]

    def erase_user(self, user_id: str) -> None:
        self.records = [record for record in self.records if record.user_id != user_id]
        self.save()

    def reset(self) -> None:
        self.records = []
        self._next_id = 1
        self.save()

    def save(self) -> None:
        self.path.write_text(
            json.dumps([asdict(record) for record in self.records], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self) -> None:
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.records = [VectorRecord(**item) for item in data]
        if self.records:
            self._next_id = max(record.record_id for record in self.records) + 1
