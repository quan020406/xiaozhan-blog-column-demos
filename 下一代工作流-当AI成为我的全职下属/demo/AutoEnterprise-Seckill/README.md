# AutoEnterprise-Seckill

用于《当 AI 成为我的全职下属》专栏的可运行工程靶场。

## 能力矩阵

| 模式 | 端点 | 用途 | 外部依赖 |
| --- | --- | --- | --- |
| unsafe | `/api/seckill/unsafe` | 演示先查后改的竞态窗口 | 无 |
| atomic | `/api/seckill/atomic` | 演示数据库条件更新 | 无 |
| redisson | `/api/seckill/redisson` | 演示分布式锁与二次校验 | Redis |

## 环境

- JDK 17+
- Maven 3.6.3+
- Python 3.11+（压测和 AI 工程脚本）
- Redis 6+（仅 Redisson 模式）

## 启动

本 Demo 不在代码里写死应用端口、服务地址或 Redis 地址。公开仓库只保留 `.env.example`，真实配置写在本机 `.env`，该文件已被 `.gitignore` 忽略，不应上传 GitHub。

| 变量 | 是否必填 | 代表什么 | 如何填写 |
| --- | --- | --- | --- |
| `SERVER_PORT` | 是 | Spring Boot 应用监听端口 | 填一个当前机器可用端口，例如你决定使用的 Web 服务端口 |
| `SECKILL_BASE_URL` | 压测时必填 | 压测脚本访问应用的基础地址 | 按 `http://<应用主机>:<SERVER_PORT>` 填写；远程部署时使用实际可访问地址 |
| `REDIS_ADDRESS` | 仅 Redisson 模式必填 | Redisson 连接 Redis 的地址 | 单机 Redis 使用 `redis://<Redis主机>:<Redis端口>`；TLS 连接使用 `rediss://<Redis主机>:<Redis端口>` |
| `REDIS_PASSWORD` | Redis 有密码时填写 | Redis 认证密码 | 只在目标 Redis 开启密码认证时设置 |

首次运行时，先复制示例配置并改成自己的环境值：

```powershell
Copy-Item .env.example .env
notepad .env
. .\scripts\load-env.ps1
```

基础模式不依赖 Redis。Spring Boot 会自动读取当前目录下的 `.env`；上面的 `load-env.ps1` 只负责把 `.env` 加载到当前 PowerShell，方便后续手工调用接口：

```powershell
mvn.cmd test
mvn.cmd spring-boot:run
```

命令要求当前终端中的 `java -version` 已指向 JDK 17 或更高版本。应用使用内存 H2，重启后数据会重置。

## Redis 模式

Redisson 模式需要提供 Redis 地址，并使用 `redis` Profile 启动：

```powershell
mvn.cmd spring-boot:run "-Dspring-boot.run.profiles=redis"
```

## AI 工程脚本

```powershell
python ai_firm\context_pruner.py --target src\main\java\com\xiaoz\seckill\service\AtomicSeckillService.java
python ai_firm\cheat_detector.py --root .
python ai_firm\start_firm.py --issue issue.txt
```

## 压测

压测脚本会自动读取当前目录下的 `.env`。`SECKILL_BASE_URL` 只给压测脚本使用，不会改变应用监听端口。

```powershell
python pipeline\run_stress_test.py --mode unsafe --concurrency 100 --requests 500 --stock 100
python pipeline\run_stress_test.py --mode atomic --concurrency 100 --requests 500 --stock 100
```
