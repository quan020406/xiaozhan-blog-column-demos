# v1_react：纯 Python ReAct 循环与函数自省注册

## 当前 Demo 目标

这个 Demo 保留最基础的 ReAct 状态机，同时补上工程边界：模型适配层、工具自省、解析失败记录和可视化 trace。默认使用 `ScriptedModel`，不需要 API Key；后续可以把模型替换为 `OpenAICompatibleModel`。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `main.py` | 演示入口，运行一个“计算预算 + 查询天气”的 ReAct 闭环，并生成 `trace.json` |
| `agent.py` | ReAct 主循环，负责 Prompt 组装、Action 解析、工具调用、Observation 回灌 |
| `tools.py` | 工具注册器与示例工具，使用 `inspect.signature` 生成工具 Schema |
| `model_clients.py` | 模型适配层，包含默认 `ScriptedModel` 和可选 OpenAI-compatible HTTP Adapter |
| `trace_recorder.py` | 结构化记录每一步模型输出、工具调用、Observation 和最终答案 |
| `visualization.html` | 独立可视化页面，读取 `trace.json` 展示状态流转 |
| `trace.json` | 运行 `main.py` 后生成的演示轨迹，不需要手工维护 |

## 运行

```powershell
python main.py
```

## 可视化

先运行 `python main.py` 生成 `trace.json`，再用浏览器打开当前目录下的 `visualization.html`。这个页面只展示 v1 的 ReAct 状态流转，不和其他 Demo 混在一起。

## 文章中可讲的工程点

- 为什么先用可控的模型替身暴露状态机，再接真实模型。
- 为什么 `temperature=0.0` 对工具调用闭环更重要。
- 为什么正则解析 `Action: name[arg]` 脆弱，并需要结构化输出或 Tool Calling 替代。

