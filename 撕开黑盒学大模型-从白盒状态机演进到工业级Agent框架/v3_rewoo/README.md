# v3_rewoo：DAG 异步调度与 ReWOO 思路

## 当前 Demo 目标

这个 Demo 保留基础串并行 benchmark，同时新增文本计划解析、依赖占位符解析、工具超时 Observation 和执行时间线。它不是完整 ReWOO 论文复现，而是一个克制版 Plan-then-Execute 架构。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `benchmark.py` | 演示入口，解析计划、分别执行串行和并行调度，并生成 `trace.json` |
| `planner.py` | 生成可读的计划文本，模拟 Planner 一次性输出 DAG |
| `parser.py` | 将 `E1: tool[arg]` 文本计划解析成结构化 `PlanStep` |
| `scheduler.py` | DAG 调度器，解析 `#E1` 依赖，支持并发执行、超时和错误 Observation |
| `worker.py` | 示例工具集合，包含正常工具和慢响应工具 |
| `trace.json` | 运行后生成的计划、耗时和时间线 |
| `visualization.html` | 独立可视化页面，展示串行与并行时间线 |

## 运行

```powershell
python benchmark.py
```

## 可视化

先运行 `python benchmark.py`，再打开当前目录下的 `visualization.html`。这个页面只展示 v3 的调度时间线，不和其他 Demo 混在一起。

## 文章中可讲的工程点

- ReAct 串行模式会把工具网络等待逐步累加。
- Plan-then-Execute 可以先生成依赖图，再并发执行无依赖节点。
- 工具失败不应该让主流程直接崩溃，可以回写错误 Observation，让后续节点看到失败事实。
- DAG 调度必须显式处理循环依赖、超时和变量替换。

