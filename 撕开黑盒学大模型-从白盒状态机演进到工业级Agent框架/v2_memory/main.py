from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from agent import MemoryAwareAgent
from memory_manager import MemoryManager, Message


ROOT = Path(__file__).resolve().parent


def serialize_results(results):
    return [
        {"score": round(score, 3), "record": asdict(record)}
        for score, record in results
    ]


def main() -> None:
    store_path = ROOT / "memory_store.json"
    manager = MemoryManager(window_size=4, threshold=0.22, store_path=store_path)
    manager.vector_store.reset()
    agent = MemoryAwareAgent(memory=manager)

    turns = [
        "我在写 Agent 专栏，关注 ReAct 状态机。",
        "请记录，第二篇要讨论记忆污染。",
        "无关信息：今天午饭吃面。",
        "继续讨论向量检索阈值。",
        "如何治理记忆污染？",
    ]
    for turn in turns:
        print(f"user: {turn}")
        print(f"assistant: {agent.chat(turn)}\n")

    manager.add(Message(role="user", content="隐私备注：用户喜欢夜跑。", user_id="guest"))
    manager.add(Message(role="user", content="噪声信息：午饭、咖啡、天气闲聊。", user_id="default"))

    query = "记忆污染 阈值 Agent"
    blind_top_k = manager.retrieve_without_threshold(query, top_k=8)
    thresholded = manager.retrieve(query, top_k=8)

    print("context snapshot:")
    print(manager.build_context(query))
    print("\nblind top-k:")
    for score, record in blind_top_k:
        print(f"{score:.2f} {record.content}")
    print("\nthresholded:")
    for score, record in thresholded:
        print(f"{score:.2f} {record.content}")

    manager.erase_user("guest")
    trace = {
        "query": query,
        "summary_memory": manager.summary_memory,
        "recent_messages": [asdict(message) for message in manager.recent_messages],
        "blind_top_k": serialize_results(blind_top_k),
        "thresholded": serialize_results(thresholded),
        "guest_records_after_erase": [
            asdict(record)
            for record in manager.vector_store.records
            if record.user_id == "guest"
        ],
    }
    (ROOT / "trace.json").write_text(
        json.dumps(trace, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\ntrace written: trace.json")


if __name__ == "__main__":
    main()
