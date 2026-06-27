# CampusHub Testing Lab

CampusHub Testing Lab 是《软件测试从入门到实战：用项目思维学测试》专栏配套的教学项目。项目以 CampusHub 校园服务协作平台为主线，内置 BookNest 图书借阅模块，用于支撑需求分析、测试用例设计、缺陷管理、接口测试、UI 自动化和性能测试练习。

当前版本覆盖第一版教学验收主线：工程骨架、登录、活动报名、BookNest 图书借阅、后台审核、测试素材和基础脚本。

## 已交付范围

- Spring Boot 后端工程，可启动并读取 H2 示例数据。
- Vue 3 + Vite + TypeScript 前端工程，可启动并展示项目概览数据。
- H2 schema 和 seed data。
- 需求文档和数据字典。
- 登录与角色权限演示。
- 活动报名和取消报名。
- BookNest 图书检索、借阅、续借、归还。
- 后台审核任务处理。
- 手工测试用例、Bug 报告样例、Postman 集合、Selenium 示例、JMeter 示例。
- 本地运行说明，不依赖本机绝对路径或真实学校数据。

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 后端 | Java 17, Spring Boot 3, Maven, H2 |
| 前端 | Vue 3, Vite, TypeScript |
| 接口 | REST JSON |
| 数据 | H2 内存数据库，启动时加载示例数据 |

## 目录结构

```text
campushub-testing-lab/
  backend/                 # Spring Boot 后端
  frontend/                # Vue 3 前端
  docs/                    # 本地需求和测试策略文档，不上传 GitHub
  scripts/                 # 发布前检查脚本
  test-assets/             # 手工用例、Bug 报告、Postman、Selenium、JMeter
```

## 后端启动

环境要求：

- JDK 17
- Maven 3.6+

启动命令：

```powershell
cd backend
mvn spring-boot:run
```

默认地址：

- API: `http://localhost:8080/api/overview`
- H2 Console: `http://localhost:8080/h2-console`
- JDBC URL: `jdbc:h2:mem:campushub`
- User: `sa`
- Password: 空

如果本机 `8080` 端口已被占用，可临时改端口启动：

```powershell
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=18080"
```

## 前端启动

环境要求：

- Node.js 18+
- npm 9+

启动命令：

```powershell
cd frontend
npm install
npm run dev
```

默认地址：`http://localhost:5173`

如后端地址不是 `http://localhost:8080`，可在启动前设置：

```powershell
$env:VITE_API_BASE_URL="http://localhost:18080"
npm run dev
```

## 示例账号

这些账号仅用于教学演示，不代表真实学校、真实用户或真实联系方式。

| 角色 | 用户名 | 密码 | 说明 |
| --- | --- | --- | --- |
| 学生 | `student01` | `campus123` | 活动报名和图书借阅练习 |
| 社团负责人 | `club01` | `campus123` | 后续活动发布练习 |
| 图书管理员 | `library01` | `campus123` | 后续 BookNest 审核练习 |
| 系统管理员 | `admin01` | `campus123` | 后续后台审核练习 |

## 当前接口

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/api/health` | 后端健康检查 |
| GET | `/api/overview` | 返回项目概览、模块、示例数据统计 |
| POST | `/api/auth/login` | 演示登录 |
| GET | `/api/books` | 返回 BookNest 示例图书 |
| GET | `/api/book-borrows` | 返回当前用户借阅记录 |
| POST | `/api/books/{bookId}/borrow` | 借阅图书 |
| POST | `/api/book-borrows/{borrowId}/renew` | 续借图书 |
| POST | `/api/book-borrows/{borrowId}/return` | 归还图书 |
| GET | `/api/activities` | 返回活动中心示例活动 |
| POST | `/api/activities/{activityId}/registrations` | 报名活动 |
| DELETE | `/api/activities/{activityId}/registrations/{username}` | 取消报名 |
| GET | `/api/admin/review-tasks` | 查询审核任务 |
| POST | `/api/admin/review-tasks/{taskId}/decision` | 处理审核任务 |

更完整的 API 契约、数据字典和测试策略文档保留在本地 `docs/`，不上传 GitHub。

## 测试素材

| 类型 | 路径 |
| --- | --- |
| 手工测试用例 | `test-assets/test-cases/activity-and-booknest-core-cases.md` |
| Bug 报告样例 | `test-assets/bug-reports/sample-book-inventory-inconsistency.md` |
| Postman 集合 | `test-assets/postman/campushub-testing-lab.postman_collection.json` |
| Selenium 示例 | `test-assets/selenium/test_login_activity_book.py` |
| JMeter 示例 | `test-assets/jmeter/campushub-activity-booknest-smoke.jmx` |

## 验收检查

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```

## 开发边界

- 不写入真实账号、手机号、邮箱、Token、Cookie。
- 不写死本机绝对路径。
- 当前登录方案是教学演示，不作为生产级认证实现。
- JMeter 脚本只提供性能测试入口，不提供通用性能结论。
- 后续如扩展场地预约、设备借用或 MySQL 持久化，应继续使用虚拟数据和可复现说明。
