# 撕开黑盒学大模型：从白盒状态机演进到工业级 Agent 框架

这是《撕开黑盒学大模型：从白盒状态机演进到工业级 Agent 框架》专栏配套代码目录。目录目标不是堆叠框架 API，而是用可读、可运行的最小工程逐步拆开 Agent 的状态流转、工具调用、记忆治理、异步调度和工业框架迁移边界。

## 目录

```text
docs/           # 本地写作稿目录，已在仓库 ignore 中排除
assets/images/  # 本地专栏封面、文章配图和生产边界图，已在仓库 ignore 中排除
v1_react/       # 纯 Python ReAct 循环、函数自省注册、trace 可视化
v2_memory/      # 长短期记忆分层治理、污染对比、擦除验证
v3_rewoo/       # 简化版 ReWOO / DAG 异步调度、超时 Observation、时间线
v4_langchain/   # LangChain / LangGraph 对照迁移与无依赖状态图
scripts/        # 专栏目录级检查脚本
```

## 专栏路线

| 期数 | 文章 | 代码入口 | 核心问题 |
| --- | --- | --- | --- |
| 0 | 拒绝做 API 调包侠：如何通过手写核心循环，建立对 Agent 框架的底层认知？ | 无新增代码 | 建立从状态机到工业框架的演进路线 |
| 1 | 大模型是如何自主调用工具的？纯 Python 实现 ReAct 引擎与函数自省注册 | `v1_react/main.py` | 工具调用闭环、函数自省、日志轨迹 |
| 2 | 拒绝盲目堆砌向量数据库：如何通过长短期记忆分层治理 Agent 的“记忆污染”？ | `v2_memory/main.py` | 滑动窗口、摘要记忆、阈值检索 |
| 3 | 告别大模型连环网络等待：用 DAG 异步调度实现 Agent 多工具并发执行 | `v3_rewoo/benchmark.py` | Planner / Worker 解耦与并发调度 |
| 4 | 源码级对照分析：当我们调用 LangChain 和 LangGraph 时，框架底层到底做了什么？ | `v4_langchain/` | 手写模块到框架抽象的映射 |
| 5 | 划清玩具与生产级系统的边界：LLM Agent 的稳定性、可观测性与生态解耦思辨 | 无新增代码 | 稳定性、持久化、安全、MCP 边界 |

## 本地运行

本目录默认不依赖真实大模型 API，也不写死本机端口、路径或私有密钥。所有示例都优先使用 Python 标准库，方便读者先观察确定性的状态流转。

```powershell
cd 撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架
python v1_react\main.py
python v2_memory\main.py
python v3_rewoo\benchmark.py
python v4_langchain\main.py
python scripts\check_portability.py
```

每个 Demo 目录都有自己的 `README.md` 和 `visualization.html`。先运行对应 Python 入口生成 `trace.json`，再打开该目录下的可视化页面；不同 Demo 不放在同一个页面里演示。

`v4_langchain/` 中保留可选依赖导入边界。未安装 LangChain / LangGraph 时，可以先运行无依赖的 `handmade_graph.py` 对照版本；安装框架后再接入真实模型与 checkpointer。

## 配套素材

文章配图和封面素材只保留在本地 `assets/images/`，不上传 GitHub。公开仓库保留生成脚本，例如 `scripts/generate_article_05_production_boundary.py`，便于需要时在本地复现素材。

## 写作约定

- 文章正文放在本地 `docs/`，该目录不上传 GitHub；公开仓库只保留读者复现实验需要的最小闭环。
- 示例默认使用 `temperature=0.0` 的确定性叙事，不在代码中硬编码真实模型 Key。
- 文中的实验数据以本机实际运行结果为准，不直接复用未复现的耗时、成功率或吞吐量。
- 生产级能力只在第 4、5 篇展开，前三篇刻意控制复杂度，优先让状态流转可观察。
