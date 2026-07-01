# 测试策略

本文档定义 CampusHub Testing Lab 01-26 教学项目的测试目标、分层策略、证据口径和发布检查入口。当前策略围绕普通业务页面、接口契约、Postman、手工用例、JUnit、Selenium 和 JMeter 素材闭环，不再依赖已移除的 QA Console 看板数据。

## 测试目标

验证教学工程是否满足以下条件：

- 学生可登录、报名活动、取消报名、提交场地预约、提交设备借用申请、查看通知、借阅图书、续借、归还和查看我的记录。
- 管理员可查看统计、库存、异常样例和审核任务，并能处理待审核任务。
- 错误密码、锁定账号、重复报名、满员报名、场地维护、场地时段冲突、无库存设备、重复设备借用、跨用户通知已读、无库存借阅、二次续借、学生越权审核等反向路径有可执行验证入口。
- OpenAPI、API 契约文档和 Postman 集合与后端实际接口一致。
- 01-26 每期文章至少能落到一个页面、接口、用例、方法表或脚本。

## 测试层级

| 层级 | 范围 | 入口 | 证据 |
| --- | --- | --- | --- |
| 后端接口测试 | 控制器与核心业务规则 | `backend` 下执行 `mvn test` | Surefire XML、JUnit 断言 |
| OpenAPI 契约 | 运行时接口描述 | `/v3/api-docs`、`/swagger-ui.html` | Swagger UI 和 OpenAPI JSON |
| Postman 接口烟测 | 正向和关键反向接口 | `test-assets/postman/campushub.postman_collection.json` | Postman/Newman 执行结果 |
| 手工测试 | 页面端到端流程 | `test-assets/test-cases/core-cases.md` | 执行记录、缺陷单 |
| UI 自动化 | 登录、活动报名、BookNest 核心流程 | `test-assets/selenium/test_login_activity_book.py` | 脚本执行日志、真实截图 |
| 性能入口 | 活动列表、图书搜索、登录后报名链路 | `test-assets/jmeter/campushub-activity-booknest-smoke.jmx`、`scripts/run_performance_probe.py` | `.jtl`、探针 CSV、执行命令 |
| 前端构建 | 普通业务页面编译和类型检查 | `frontend` 下执行 `npm run build` | Vite 构建结果 |
| 发布检查 | 目录、隐私、路径和脚本结构 | 项目根执行 `python scripts/check_release.py` | 检查脚本输出 |

## 接口测试范围

| 模块 | 必测正向路径 | 必测反向路径 |
| --- | --- | --- |
| 系统 | 健康检查、项目概览 | 后端未启动时由运行环境暴露连接失败，不写入业务断言 |
| 账号 | `student01` 登录成功 | 密码错误返回 `401`；锁定账号返回 `403` |
| 活动 | 查询活动、报名开放活动、取消报名 | 重复报名返回 `409`；满员活动返回 `409` |
| 场地预约 | 查询场地、查询我的预约、提交预约 | 维护中场地返回 `409`；重叠时段返回 `409` |
| 设备借用 | 查询设备、查询我的借用、提交借用申请 | 无库存设备返回 `409`；重复借用同一设备返回 `409` |
| 消息通知 | 查询通知、标记本人通知已读 | 跨用户通知标记返回 `404` |
| BookNest | 查询图书、查询借阅、借阅、续借、归还 | 无库存返回 `409`；二次续借返回 `409` |
| 后台审核 | 查询审核任务、管理员审核通过 | 学生审核返回 `403`；非法审核结果返回 `400` |

## 证据口径

- 未执行的 Selenium、JMeter 或性能探针只能称为“脚本设计”或“待执行验证”。
- 执行过的结果必须记录环境、命令、输入数据和边界说明。
- 性能探针和 JMeter 样例只服务教学，不能得出通用性能结论。
- 截图必须来自真实运行，不能用占位图冒充执行证据。

## 不做的事

- 不给出通用性能结论。
- 不把演示登录方案描述为生产安全方案。
- 不接入真实短信、邮件、支付或统一身份认证。
- 不使用真实学校、真实用户、真实联系方式或生产数据。
- 不在文章中伪造 Selenium 截图、JMeter 结果或接口执行记录。

## 验收命令

建议从 `campushub-testing-lab` 目录执行：

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```

接口契约本地验证：

```powershell
cd backend
mvn spring-boot:run
```

启动后打开：

- `http://localhost:8080/swagger-ui.html`
- `http://localhost:8080/v3/api-docs`

Postman 集合可使用 `baseUrl = http://localhost:8080` 执行。执行前建议重启后端，让 H2 数据回到初始状态。
