# v2_memory：长短期记忆分层治理

## 当前 Demo 目标

这个 Demo 保留基础的 `recent_messages + summary_memory + vector_memory` 三轨结构，并新增可复现实验：同一查询分别走无阈值 Top-K 和阈值过滤，观察噪声记忆如何进入上下文。默认使用本地 JSON 存储模拟向量库接口，不引入外部服务。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `main.py` | 演示入口，写入多轮对话、污染噪声和跨用户隐私记录，并生成 `trace.json` |
| `agent.py` | 一个最小记忆感知 Agent，用于展示上下文如何影响回答 |
| `memory_manager.py` | 三轨制记忆管理器，负责短期窗口、摘要压缩、阈值检索和用户擦除 |
| `vector_store.py` | 本地 JSON 向量库门面，提供 add/search/erase/reset；当前用词频余弦作为无依赖 fallback |
| `memory_store.json` | 运行后生成的本地持久化记忆数据 |
| `trace.json` | 运行后生成的污染对比和擦除验证结果 |
| `visualization.html` | 独立可视化页面，展示短期窗口、摘要记忆、Top-K 污染对比和用户擦除结果 |

## 运行

```powershell
python main.py
```

## 可视化

先运行 `python main.py`，再打开当前目录下的 `visualization.html`。这个页面只展示 v2 的记忆治理结果，不和其他 Demo 混在一起。

## 文章中可讲的工程点

- Top-K 不是越多越好，无阈值召回会把低相关噪声塞回上下文。
- 短期窗口解决连续对话，摘要记忆解决早期上下文压缩，向量记忆解决长期检索。
- 多用户场景下必须按 `user_id` 隔离检索，并支持主动擦除。
- 当前 `JsonVectorStore` 是无依赖 fallback，后续可以替换为 ChromaDB / FAISS，而不改上层 `MemoryManager` 语义。

