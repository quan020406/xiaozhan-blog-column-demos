# JMeter 示例脚本

## 用途

`campushub-activity-booknest-smoke.jmx` 是第一版性能测试入口脚本，覆盖：

- 健康检查接口。
- 活动列表接口。
- 场地列表接口。
- 设备列表接口。
- 通知列表接口。
- 图书检索接口。

该脚本不提供性能结论，只提供可导入、可配置、可扩展的压测起点。

## 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `HOST` | `localhost` | 后端主机 |
| `PORT` | `8080` | 后端端口 |
| `THREADS` | `5` | 并发线程数 |
| `LOOPS` | `3` | 每个线程循环次数 |

命令行示例：

```powershell
jmeter -n -t campushub-activity-booknest-smoke.jmx -JHOST=localhost -JPORT=8080 -JTHREADS=5 -JLOOPS=3 -l ..\reports\jmeter-latest.jtl
```

如果本机没有安装 JMeter，可使用项目内置探针生成 JMeter 兼容 `.jtl`，该方式会真实请求本地后端接口，但不替代正式 JMeter 压测：

```powershell
cd ..\..
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

生成结果：

```text
test-assets/reports/jmeter-latest.jtl
```
