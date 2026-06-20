# 手写实现与 LangChain / LangGraph 对照

| 手写实现 | 框架迁移点 | 迁移后收益 |
| --- | --- | --- |
| `v1_react.ToolRegistry` | LangChain `@tool` / tool calling | 标准化工具 Schema，减少模型适配分支 |
| `v1_react.ReactAgent.run` | LangGraph node + conditional edge | 状态流转显式化，便于调试复杂分支 |
| `v2_memory.MemoryManager.recent_messages` | Messages state | 使用框架标准消息结构和裁剪能力 |
| `v2_memory.summary_memory` | summarization node | 将压缩过程变成可观测、可重试的图节点 |
| `v2_memory.vector_memory` | retriever / vector store | 复用向量库连接器和检索接口 |
| `v3_rewoo.scheduler` | LangGraph 并行分支 / durable execution | 获得持久化、恢复和更清晰的执行边界 |
| `handmade_graph.MiniStateGraph` | LangGraph `StateGraph` | 用无依赖方式解释节点、边、条件路由和状态快照 |

## 迁移原则

先确认手写版本里的状态、输入、输出和失败语义，再映射到框架抽象。不要把框架当成黑盒替换，而是把它看作对已理解机制的工程封装。

## 当前目录的分层

- `handmade_graph.py`：教学层，保证读者不安装框架也能理解状态图抽象。
- `langchain_agent.py` / `langgraph_agent.py`：适配层，安装依赖后再连接真实框架。
- `visualization.html`：展示状态推进轨迹，辅助文章说明框架为什么需要 checkpointer / persistence。

