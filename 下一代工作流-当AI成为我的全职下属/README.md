# 下一代工作流：当 AI 成为我的全职下属

这是《下一代工作流：当 AI 成为我的全职下属》专栏配套 Demo 目录，保留可运行的 `AutoEnterprise-Seckill` 高并发秒杀 Demo、配套素材和工程治理脚本。

## 目录

```text
demo/AutoEnterprise-Seckill/   # Spring Boot + MyBatis-Plus + Redisson Demo
scripts/                        # 专栏目录级检查脚本
```

## 动画辅助理解

第三期《AI Agent 防作弊 CI 实战》配套 3 个 GIF 和 3 个完整 HTML 动画页：

- [第三期动画索引页](../animations/article-03/)
- [CI 流水线拦截动画](../animations/article-03/ci-gate.html)
- [假绿色流水线对比动画](../animations/article-03/fake-green.html)
- [只读门禁权限边界动画](../animations/article-03/readonly-gate.html)
- [iframe 调用片段](../animations/article-03/iframe-snippets.md)

文章配图和封面素材只保留在本地 `assets/images/`，不上传 GitHub。生成脚本保留在 `scripts/`，便于本地复现素材来源。

## 运行 Demo

本仓库不在代码里写死应用端口、服务地址或 Redis 地址。公开仓库只保留 `demo/AutoEnterprise-Seckill/.env.example`，真实配置写在本机 `demo/AutoEnterprise-Seckill/.env`，该文件已被 `.gitignore` 忽略，不应上传 GitHub。

| 变量 | 是否必填 | 代表什么 | 如何填写 |
| --- | --- | --- | --- |
| `SERVER_PORT` | 是 | Spring Boot 应用监听端口 | 填一个当前机器可用端口，例如你决定使用的 Web 服务端口 |
| `SECKILL_BASE_URL` | 压测/接口调用时必填 | 压测脚本和手工请求访问应用的基础地址 | 按 `http://<应用主机>:<SERVER_PORT>` 填写；如果应用部署在网关或远程服务器，使用实际可访问地址 |
| `REDIS_ADDRESS` | 仅 Redisson 模式必填 | Redisson 连接 Redis 的地址 | 单机 Redis 使用 `redis://<Redis主机>:<Redis端口>`；TLS 连接使用 `rediss://<Redis主机>:<Redis端口>` |
| `REDIS_PASSWORD` | Redis 有密码时填写 | Redis 认证密码 | 只在目标 Redis 开启密码认证时设置 |

首次运行时，先复制示例配置并改成自己的环境值：

```powershell
cd demo\AutoEnterprise-Seckill
Copy-Item .env.example .env
notepad .env
. .\scripts\load-env.ps1
```

基础模式不依赖 Redis。Spring Boot 会自动读取当前目录下的 `.env`；上面的 `load-env.ps1` 只负责把 `.env` 加载到当前 PowerShell，方便后续手工调用接口：

```powershell
mvn.cmd test
mvn.cmd spring-boot:run
```

应用启动后，使用 `.env` 中的 `SECKILL_BASE_URL` 调用接口：

```powershell
Invoke-RestMethod "$env:SECKILL_BASE_URL/api/products/1"
Invoke-RestMethod -Method Post "$env:SECKILL_BASE_URL/api/admin/reset?stock=100"
```

压测示例：

```powershell
python pipeline\run_stress_test.py --mode unsafe --concurrency 100 --requests 500 --stock 100
python pipeline\run_stress_test.py --mode atomic --concurrency 100 --requests 500 --stock 100
```

Redis 为可选能力。Redisson 模式需要额外提供 Redis 地址，并使用 `redis` Profile 启动应用：

```powershell
mvn.cmd spring-boot:run "-Dspring-boot.run.profiles=redis"
```

## 说明

- 本目录不上传文章正文和写作过程文档，只保留读者复现实验需要的 Demo 内容。
- 文中的实验结果应以本机实际执行结果为准，不建议直接填写未经复现的吞吐量或成功率。
- 运行 Demo 前请优先查看 `demo/AutoEnterprise-Seckill/README.md`。
