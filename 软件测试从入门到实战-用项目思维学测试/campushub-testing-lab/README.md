# CampusHub Testing Lab

CampusHub Testing Lab 是《软件测试从入门到实战：用项目思维学测试》的配套示范项目。它用 CampusHub 校园服务协作平台和内置 BookNest 图书借阅模块，承接需求分析、用例设计、缺陷管理、接口测试、UI 自动化、性能测试和质量看板文章素材。

如果你只是想跟着博客看一个真实一点的测试对象，不需要一开始就理解所有目录。先按下面的读者路线走。

## 读者 10 分钟路线

1. 启动后端：

```powershell
cd backend
mvn spring-boot:run
```

2. 启动前端：

```powershell
cd frontend
npm install
npm run dev
```

3. 打开页面：

```text
http://localhost:5173
```

4. 用学生账号登录：

```text
student01 / campus123
```

5. 先看 **QA Command Center**，再打开一份测试素材：

```text
test-assets/test-cases/activity-and-booknest-core-cases.md
test-assets/bug-reports/sample-book-inventory-inconsistency.md
```

## 三种使用模式

| 读者目标 | 需要做什么 | 推荐入口 |
| --- | --- | --- |
| 只读文章 | 不启动项目，先看截图、用例、Bug 样例和接口说明 | 本 README 的“只看不跑” |
| 跑业务系统 | 启动后端和前端，体验登录、报名、预约、借用、借阅和审核 | 本 README 的“5 分钟启动” |
| 跑测试证据 | 在业务系统启动后执行 Selenium、性能探针并刷新看板 | 本 README 的“测试资产怎么用” |

## 本地环境检查

如果你不确定机器上有没有 Java、Maven、Node、npm、Python，可以先运行轻量检查脚本。它只检查工具是否可用，并提示下一步命令，不会启动服务，也不会强制跑 Selenium 或 JMeter。

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify_local.ps1
```

跨平台：

```powershell
python scripts\verify_local.py
```

## 只看不跑

暂时不装 Java / Node 也可以先看这些材料：

| 想了解什么 | 建议打开 |
| --- | --- |
| QA Command Center 页面效果 | `frontend/src/assets/test-assets/screenshots/selenium-login.png`、`frontend/src/assets/test-assets/screenshots/selenium-booknest.png` |
| 自动化执行截图 | `frontend/src/assets/test-assets/screenshots/selenium-activity.png`、`frontend/src/assets/test-assets/screenshots/selenium-room.png`、`frontend/src/assets/test-assets/screenshots/selenium-device.png`、`frontend/src/assets/test-assets/screenshots/selenium-notification.png` |
| 示例测试用例 | `test-assets/test-cases/activity-and-booknest-core-cases.md` |
| 示例 Bug 报告 | `test-assets/bug-reports/sample-book-inventory-inconsistency.md` |
| 接口契约 | `docs/api-contract.md` |
| 测试策略 | `docs/test-strategy.md` |
| 看板数据结构 | `frontend/src/assets/test-assets/test-dashboard.json` |

示例接口返回可以在后端启动后访问：

```text
GET http://localhost:8080/api/overview
GET http://localhost:8080/api/activities?username=student01
GET http://localhost:8080/api/books?keyword=测试
```

## 文章和项目文件映射

| 文章主题 | 建议读者打开的文件 |
| --- | --- |
| 需求分析 | `docs/requirements.md`、`docs/data-dictionary.md` |
| 测试策略 | `docs/test-strategy.md` |
| 用例设计 | `test-assets/test-cases/activity-and-booknest-core-cases.md` |
| 缺陷管理 | `test-assets/bug-reports/sample-book-inventory-inconsistency.md` |
| 接口测试 | `docs/api-contract.md`、`test-assets/postman/campushub-testing-lab.postman_collection.json` |
| UI 自动化测试 | `test-assets/selenium/test_login_activity_book.py`、`frontend/src/assets/test-assets/screenshots/` |
| 性能测试入门 | `test-assets/jmeter/campushub-activity-booknest-smoke.jmx`、`scripts/run_performance_probe.py`、`test-assets/reports/jmeter-latest.jtl` |
| 质量看板 | `scripts/generate_test_dashboard.py`、`frontend/src/assets/test-assets/test-dashboard.json` |

更细的文章素材映射见：

```text
test-assets/article-evidence-map.md
```

## 环境要求

| 工具 | 建议版本 | 用途 |
| --- | --- | --- |
| JDK | 17 | 启动 Spring Boot 后端 |
| Maven | 3.6+ | 构建和测试后端 |
| Node.js | 18+ | 启动 Vue 前端 |
| npm | 9+ | 安装前端依赖 |
| Python | 3.10+ | 运行看板生成、Selenium 和性能探针脚本 |
| Chrome | 当前稳定版 | 运行 Selenium UI 自动化 |

## 5 分钟启动

打开两个终端，分别启动后端和前端。

### 1. 启动后端

```powershell
cd backend
mvn spring-boot:run
```

默认后端地址：

- API 健康检查：`http://localhost:8080/api/health`
- Swagger UI：`http://localhost:8080/swagger-ui.html`
- OpenAPI JSON：`http://localhost:8080/v3/api-docs`
- H2 Console：`http://localhost:8080/h2-console`

H2 Console 连接信息：

| 项 | 值 |
| --- | --- |
| JDBC URL | `jdbc:h2:mem:campushub` |
| User Name | `sa` |
| Password | 留空 |

如果 `8080` 被占用，改用 18080：

```powershell
cd backend
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=18080"
```

### 2. 启动前端

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
npm install
npm run dev
```

前端通过 Vite 代理访问 `/api`。不要直接用浏览器跨域调用后端接口调试页面，否则可能遇到跨域限制。

## 页面怎么用

启动后默认进入 **QA Command Center**。

| 区域 | 用途 |
| --- | --- |
| 质量控制台 | 查看质量门禁、风险队列、性能趋势、自动化截图、测试用例和执行摘要 |
| 活动 / BookNest / 审核 | 演示登录、活动报名、场地预约、设备借用、图书借阅、消息通知和后台审核 |
| 用例与缺陷证据 | 查看测试用例、缺陷样例、脚本和报告的证据映射 |

建议使用顺序：

1. 先看 **质量控制台**，了解当前项目质量状态。
2. 切到 **活动 / BookNest / 审核**。
3. 使用学生账号登录，尝试活动报名、场地预约、设备借用、图书借阅和通知已读。
4. 使用管理员账号登录，处理后台审核任务。
5. 回到 **质量控制台**，查看自动化截图、性能趋势和执行摘要。

## 示例账号

所有示例账号仅用于教学演示，不代表真实学校、真实用户或生产认证方案。

| 角色 | 用户名 | 密码 | 可练习内容 |
| --- | --- | --- | --- |
| 学生 | `student01` | `campus123` | 活动报名、场地预约、设备借用、BookNest 借阅、通知查看 |
| 学生 | `student02` | `campus123` | UI 自动化默认演示账号 |
| 社团负责人 | `club01` | `campus123` | 活动和设备相关数据观察 |
| 图书管理员 | `library01` | `campus123` | BookNest 相关数据观察 |
| 系统管理员 | `admin01` | `campus123` | 后台审核任务处理 |

## 接口怎么用

后端启动后，可以通过 Swagger UI 或 Postman 调用接口。

| 方式 | 入口 |
| --- | --- |
| Swagger UI | `http://localhost:8080/swagger-ui.html` |
| OpenAPI JSON | `http://localhost:8080/v3/api-docs` |
| Postman 集合 | `test-assets/postman/campushub-testing-lab.postman_collection.json` |
| API 契约说明 | `docs/api-contract.md` |

主要接口：

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/api/health` | 后端健康检查 |
| GET | `/api/overview` | 项目概览和示例数据统计 |
| POST | `/api/auth/login` | 演示登录 |
| GET | `/api/activities` | 活动列表 |
| POST | `/api/activities/{activityId}/registrations` | 活动报名 |
| DELETE | `/api/activities/{activityId}/registrations/{username}` | 取消报名 |
| GET | `/api/rooms` | 场地列表 |
| POST | `/api/rooms/{roomId}/reservations` | 提交场地预约 |
| GET | `/api/devices` | 设备列表 |
| POST | `/api/devices/{deviceId}/borrow` | 提交设备借用 |
| GET | `/api/notifications` | 用户通知 |
| POST | `/api/notifications/{notificationId}/read` | 标记通知已读 |
| GET | `/api/books` | BookNest 图书列表 |
| POST | `/api/books/{bookId}/borrow` | 图书借阅 |
| POST | `/api/book-borrows/{borrowId}/renew` | 图书续借 |
| POST | `/api/book-borrows/{borrowId}/return` | 图书归还 |
| GET | `/api/admin/review-tasks` | 审核任务列表 |
| POST | `/api/admin/review-tasks/{taskId}/decision` | 处理审核任务 |

## 测试资产怎么用

### 后端测试

```powershell
cd backend
mvn test
```

### 前端构建检查

```powershell
cd frontend
npm run build
```

### Selenium UI 自动化

先确保后端和前端都已启动，再执行：

```powershell
pip install -r test-assets\selenium\requirements.txt
python test-assets\selenium\test_login_activity_book.py --base-url http://127.0.0.1:5173
```

脚本覆盖登录、活动报名、场地预约、设备借用、BookNest 借阅和通知已读。

输出文件：

```text
test-assets/reports/selenium-latest.json
frontend/src/assets/test-assets/screenshots/selenium-login.png
frontend/src/assets/test-assets/screenshots/selenium-activity.png
frontend/src/assets/test-assets/screenshots/selenium-room.png
frontend/src/assets/test-assets/screenshots/selenium-device.png
frontend/src/assets/test-assets/screenshots/selenium-booknest.png
frontend/src/assets/test-assets/screenshots/selenium-notification.png
```

### JMeter 和性能探针

JMeter 脚本入口：

```text
test-assets/jmeter/campushub-activity-booknest-smoke.jmx
```

如果本机没有安装 JMeter，可以用内置性能探针生成看板可读取的 `.jtl`：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

如果后端使用 18080：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:18080 --loops 5
```

输出文件：

```text
test-assets/reports/jmeter-latest.jtl
```

### 刷新 QA Console 看板

当 Selenium 或性能探针生成新结果后，运行：

```powershell
python scripts\generate_test_dashboard.py
```

看板数据会写入：

```text
frontend/src/assets/test-assets/test-dashboard.json
```

刷新浏览器后，QA Command Center 会展示最新截图、性能趋势和执行摘要。

## 发布前检查

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```

在专栏根目录还可以执行结构检查：

```powershell
cd ..
python scripts\check_column.py
```

## 目录结构

```text
campushub-testing-lab/
  backend/                 # Spring Boot 后端
  frontend/                # Vue 3 前端与 QA Command Center
  docs/                    # API、需求、测试策略和数据字典
  scripts/                 # 环境检查、看板生成、性能探针、发布检查
  test-assets/             # 用例、Bug、Postman、Selenium、JMeter、报告
  CONTRIBUTING.md          # 贡献说明
  FAQ.md                   # 常见问题
  LEARNING_PATH.md         # 学习路线
  RELEASE_CHECKLIST.md     # 发布前检查清单
```

## 常见问题入口

- 启动失败、端口冲突、H2 数据重置、Selenium 和性能测试说明见 `FAQ.md`。
- 学习顺序见 `LEARNING_PATH.md`。
- 贡献范围和提交边界见 `CONTRIBUTING.md`。
- 发布前证据检查见 `RELEASE_CHECKLIST.md`。

## 开发边界

- 不写入真实账号、手机号、邮箱、Token、Cookie 或真实学校数据。
- 不提交本机绝对路径、私有代理、IDE 缓存、构建产物、日志和依赖目录。
- 当前登录方案是教学演示，不作为生产级认证实现。
- 性能脚本只提供入门练习和本机样例证据，不提供通用性能结论。
