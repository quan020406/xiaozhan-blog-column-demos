# v4_langchain：手写实现到 LangChain / LangGraph 的迁移对照

## 当前 Demo 目标

这个目录分成两层：一层是可选的真实 LangChain / LangGraph 适配文件；另一层是无依赖的 `MiniStateGraph`，用于可运行地解释节点、边、条件路由和状态快照。这样即使本机没有安装框架，也能先观察框架抽象解决了什么问题。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `main.py` | 演示入口，运行无依赖 `MiniStateGraph` 并生成 `trace.json` |
| `handmade_graph.py` | 手写小型状态图执行器，对照 LangGraph 的 node、edge、conditional edge、state |
| `langchain_agent.py` | 可选 LangChain tools 适配示例，未安装依赖时会给出明确错误 |
| `langgraph_agent.py` | 可选 LangGraph `StateGraph` 适配示例，未安装依赖时会给出明确错误 |
| `compare_with_handmade.md` | 手写模块与框架抽象的对照表 |
| `trace.json` | 运行后生成的节点状态快照 |
| `visualization.html` | 独立可视化页面，展示状态图节点执行顺序 |

## 运行

```powershell
python main.py
```

## 可视化

先运行 `python main.py`，再打开当前目录下的 `visualization.html`。这个页面只展示 v4 的框架抽象对照，不和其他 Demo 混在一起。

## 文章中可讲的工程点

- `while True` 循环可以迁移为节点和条件边。
- 中间状态从局部变量变成显式 `state`，更适合持久化、恢复和调试。
- LangGraph 的价值不只是“画图”，而是把 long-running agent 的状态推进过程标准化。
- 真实框架适配层要放在边界上，不应该污染前三篇手写原理 Demo。

