# JMeter 示例脚本

本目录承接第 25-26 期文章。脚本用于教学演示，不代表性能结论。

当前 `.jmx` 包含登录请求、`token` 提取、活动列表、图书搜索和活动报名链路。后端示例接口暂不强制校验该 `token`，脚本仍保留 `Authorization: Bearer ${authToken}`，用于讲解登录态提取、请求头传递和链路断言。

## 命令行执行

```powershell
jmeter -n -t test-assets\jmeter\campushub-activity-booknest-smoke.jmx -JHOST=localhost -JPORT=8080 -l test-assets\reports\jmeter-latest.jtl
```

如果本机没有 JMeter，可以先用项目内置探针理解响应时间、成功率和样本数：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

所有结果都只能作为本机练习样例。正式性能结论必须补充机器配置、数据量、并发模型和多轮结果。

报名请求会修改 H2 示例数据。重复执行前建议重启后端或恢复初始数据，否则可能因为重复报名返回冲突，这属于测试数据状态变化，不应直接写成性能失败。
