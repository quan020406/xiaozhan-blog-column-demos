# CampusHub Testing Lab

CampusHub Testing Lab 是《软件测试从入门到实战：用项目思维学测试》的可运行配套工程。它用一个校园服务协作平台，把博客文章里的测试概念落到真实页面、接口、数据和测试资产上。

项目目标不是模拟完整商业系统，而是提供一个足够完整、可本地运行、适合测试新人练习的教学项目。

## 你可以练什么

- 需求分析：从活动报名、图书借阅、场地预约、设备借用中识别规则和风险。
- 用例设计：把登录、容量、库存、状态流转和权限差异转成测试用例。
- 缺陷管理：基于可复现样例编写 Bug 报告。
- 接口测试：使用 Swagger/OpenAPI 或 Postman 调用核心接口。
- UI 自动化：用 Selenium 跑登录、活动报名和 BookNest 借阅链路。
- 性能测试入门：用 JMeter 和性能探针理解响应时间、并发和断言。

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 后端 | Java 17、Spring Boot 3、Maven、H2、springdoc-openapi、JUnit 5 |
| 前端 | Vue 3、Vite、TypeScript、lucide-vue-next |
| 测试资产 | Postman、Selenium、JMeter、Python Playwright 烟测脚本 |

## 10 分钟启动

### 1. 检查环境

在 `campushub-testing-lab/` 目录执行：

```powershell
python scripts\verify_local.py
```

推荐环境：

| 工具 | 建议版本 |
| --- | --- |
| Java | 17+ |
| Maven | 3.8+ |
| Node.js | 18+ |
| npm | 9+ |
| Python | 3.10+ |

### 2. 启动后端

```powershell
cd backend
mvn spring-boot:run
```

默认地址：

| 入口 | 地址 |
| --- | --- |
| 健康检查 | `http://localhost:8080/api/health` |
| Swagger UI | `http://localhost:8080/swagger-ui.html` |
| OpenAPI JSON | `http://localhost:8080/v3/api-docs` |
| H2 Console | `http://localhost:8080/h2-console` |

如果 `8080` 被占用：

```powershell
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=18080"
```

### 3. 启动前端

后端使用默认 `8080` 时：

```powershell
cd frontend
npm install
npm run dev
```

浏览器访问：

```text
http://localhost:5173
```

如果后端改到 `18080`，前端启动前设置代理目标：

```powershell
cd frontend
$env:VITE_API_BASE_URL="http://localhost:18080"
npm run dev
```

如果你要用生产构建或静态预览直接访问后端，可以设置：

```powershell
$env:VITE_DIRECT_API_BASE_URL="http://localhost:8080"
```

## 示例账号

所有账号和数据均为教学虚拟数据。

| 角色 | 用户名 | 密码 | 可练习内容 |
| --- | --- | --- | --- |
| 学生 | `student01` | `campus123` | 登录、活动报名、BookNest 借阅、场地预约、设备借用、我的记录 |
| 学生 | `student02` | `campus123` | 数据隔离、自动化脚本默认账号和记录归属验证 |
| 管理员 | `admin01` | `campus123` | 统计、库存、异常样例、审核任务和权限差异 |

## 推荐体验路径

1. 使用 `student01 / campus123` 登录。
2. 打开“活动列表”，执行一次活动报名或取消报名。
3. 打开“图书列表”，搜索图书并借阅一本有库存图书。
4. 打开“我的记录”，确认报名、借阅、预约和设备借用记录。
5. 打开“场地预约”，观察维护场地、日期和冲突时段限制。
6. 打开“设备借用”，提交一次设备借用申请。
7. 打开“消息通知”，标记通知为已读。
8. 使用 `admin01 / campus123` 登录，打开“管理员入口”查看审核任务。
9. 打开“测试素材”，对照需求、用例、Bug、接口、Selenium 和 JMeter 材料。

## 核心测试资产

| 资产 | 文件 |
| --- | --- |
| 需求说明 | `docs/requirements.md` |
| API 契约 | `docs/api-contract.md` |
| 数据字典 | `docs/data-dictionary.md` |
| 测试策略 | `docs/test-strategy.md` |
| 手工测试用例 | `test-assets/test-cases/core-cases.md` |
| Bug 报告样例 | `test-assets/bug-reports/sample-activity-registration-full.md` |
| 已知教学缺陷 | `test-assets/known-defects.md` |
| Postman 集合 | `test-assets/postman/campushub.postman_collection.json` |
| Selenium 脚本 | `test-assets/selenium/test_login_activity_book.py` |
| JMeter 脚本 | `test-assets/jmeter/campushub-activity-booknest-smoke.jmx` |
| 01-26 素材追踪 | `test-assets/article-evidence-map.md` |
| 方法表补充 | `test-assets/article-deliverables/03-24-method-tables.md` |

## 常用接口

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| `POST` | `/api/auth/login` | 登录 |
| `GET` | `/api/activities` | 活动列表和我的报名状态 |
| `POST` | `/api/activities/{activityId}/registrations` | 活动报名 |
| `DELETE` | `/api/activities/{activityId}/registrations/{username}` | 取消报名 |
| `GET` | `/api/books` | 图书列表和搜索 |
| `POST` | `/api/books/{bookId}/borrow` | 图书借阅 |
| `GET` | `/api/book-borrows` | 我的借阅 |
| `POST` | `/api/book-borrows/{borrowId}/renew` | 图书续借 |
| `POST` | `/api/book-borrows/{borrowId}/return` | 图书归还 |
| `GET` | `/api/rooms` | 场地列表 |
| `POST` | `/api/rooms/{roomId}/reservations` | 提交场地预约 |
| `GET` | `/api/devices` | 设备列表 |
| `POST` | `/api/devices/{deviceId}/borrow` | 提交设备借用 |
| `GET` | `/api/notifications` | 消息通知 |
| `POST` | `/api/notifications/{notificationId}/read` | 标记已读 |
| `GET` | `/api/admin/review-tasks` | 审核任务 |
| `POST` | `/api/admin/review-tasks/{taskId}/decision` | 处理审核任务 |
| `GET` | `/api/overview` | 项目概览 |

## 本地验证

后端测试：

```powershell
cd backend
mvn test
```

前端构建：

```powershell
cd frontend
npm run build
```

发布检查：

```powershell
python scripts\check_release.py
python scripts\check_completion.py
```

页面烟测需要先启动后端和前端：

```powershell
python scripts\check_ui_smoke.py --base-url http://127.0.0.1:5173
```

性能探针需要先启动后端：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

性能探针输出在 `test-assets/reports/`，该目录是本地运行产物，不建议提交。

## 目录结构

```text
campushub-testing-lab/
  backend/                 # Spring Boot 后端
  frontend/                # Vue 3 前端
  docs/                    # 工程需求、接口、数据字典和测试策略
  scripts/                 # 环境检查、发布检查、烟测和性能探针
  test-assets/             # 用例、Bug、Postman、Selenium、JMeter 和文章映射
  CONTRIBUTING.md
  FAQ.md
  LEARNING_PATH.md
  RELEASE_CHECKLIST.md
```

## 发布边界

- 本项目只使用虚拟教学数据。
- 当前登录方案是教学演示，不是生产认证方案。
- Selenium 和 JMeter 资产用于学习测试设计和脚本结构，不输出未经验证的性能结论。
- 不提交 `.env`、Token、Cookie、真实账号、真实手机号、真实邮箱、真实学校数据、本机绝对路径或私有代理。
- 不提交 `node_modules/`、`dist/`、`target/`、日志、缓存和运行报告。

## 相关文档

- [学习路线](./LEARNING_PATH.md)
- [FAQ](./FAQ.md)
- [贡献指南](./CONTRIBUTING.md)
- [发布前检查清单](./RELEASE_CHECKLIST.md)
