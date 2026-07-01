# API 契约

本文档记录 CampusHub Testing Lab 01-26 教学项目接口契约，用于接口测试、Postman 集合维护、后续报告生成脚本和文章素材引用。当前接口基于本地教学项目，不接入真实身份认证、短信、邮件或生产数据。

## 访问入口

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| API 默认地址 | `http://localhost:8080` | 后端默认端口 |
| OpenAPI JSON | `http://localhost:8080/v3/api-docs` | Springdoc 自动生成的 OpenAPI 描述 |
| Swagger UI | `http://localhost:8080/swagger-ui.html` | 浏览器交互式接口文档 |
| H2 Console | `http://localhost:8080/h2-console` | 本地内存库调试入口 |

所有业务接口以 `/api` 开头，默认请求和响应格式为 JSON。当前登录接口返回 `demo-token-*` 演示 token，不作为生产鉴权方案。

## 示例账号

| 角色 | 用户名 | 密码 | 用途 |
| --- | --- | --- | --- |
| 学生 | `student01` | `campus123` | 活动报名、图书借阅 |
| 学生 | `student02` | `campus123` | 反向和重复操作隔离样例 |
| 锁定学生 | `student_locked` | `campus123` | 登录失败和权限边界 |
| 图书管理员 | `library01` | `campus123` | BookNest 后续扩展 |
| 后勤管理员 | `logistics01` | `campus123` | 场地和设备扩展样例 |
| 系统管理员 | `admin01` | `campus123` | 后台审核 |

## 通用错误

Spring Boot 默认错误响应包含 `status`、`error`、`path` 等字段。测试断言优先检查 HTTP 状态码和核心业务提示，不依赖完整错误 JSON 结构。

| 状态码 | 场景 | 当前示例 |
| --- | --- | --- |
| 400 | 请求参数不合法 | 审核结果不是 `APPROVED` 或 `REJECTED` |
| 401 | 账号或密码错误 | 登录密码错误 |
| 403 | 账号锁定或角色无权限 | 锁定账号登录、学生处理审核任务 |
| 404 | 资源不存在 | 活动、图书或借阅记录不存在 |
| 409 | 业务规则冲突 | 重复报名、满员报名、场地维护、场地时段冲突、无库存借阅、二次续借 |

## 系统接口

### GET `/api/health`

用途：后端健康检查。

响应示例：

```json
{
  "status": "UP",
  "project": "campushub-testing-lab"
}
```

### GET `/api/overview`

用途：返回项目概览、模块清单和示例数据统计。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `project` | string | 项目名称 |
| `version` | string | 教学项目版本 |
| `modules[]` | array | 模块名称、范围和测试价值 |
| `statistics` | object | 用户、活动、图书、场地、设备数量 |

## 账号接口

### POST `/api/auth/login`

用途：演示登录并返回角色权限。

请求：

```json
{
  "username": "student01",
  "password": "campus123"
}
```

成功响应：

```json
{
  "token": "demo-token-student01",
  "user": {
    "id": 1,
    "username": "student01",
    "displayName": "测试学生一号",
    "roleCode": "STUDENT",
    "passwordHint": "campus123",
    "status": "ACTIVE",
    "failedLoginCount": 0
  },
  "permissions": ["ACTIVITY_READ", "ACTIVITY_REGISTER", "BOOK_READ", "BOOK_BORROW"]
}
```

核心规则：

- 只有 `ACTIVE` 用户可以登录。
- 密码错误返回 `401`，并增加失败次数。
- 锁定用户返回 `403`。
- 成功登录会写入审计日志。

## 活动接口

### GET `/api/activities?username=student01`

用途：查询活动列表，并标记当前用户是否已报名。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 活动 ID |
| `title` | string | 活动名称 |
| `organizer` | string | 组织方 |
| `location` | string | 地点 |
| `capacity` | number | 名额上限 |
| `registeredCount` | number | 已报名人数 |
| `status` | string | `OPEN` 或 `FULL` |
| `registered` | boolean | 当前用户是否已报名 |

### POST `/api/activities/{activityId}/registrations`

用途：学生报名活动。

请求：

```json
{
  "username": "student02"
}
```

成功响应：

```json
{
  "code": "ACTIVITY_REGISTERED",
  "message": "活动报名成功"
}
```

核心规则：

- 活动必须存在且状态为 `OPEN`。
- 已报名人数必须小于名额上限。
- 同一用户不能重复报名同一活动。
- 报名成功后写入报名记录、增加人数、生成通知并写入审计日志。

### DELETE `/api/activities/{activityId}/registrations/{username}`

用途：取消活动报名。

成功响应：

```json
{
  "code": "ACTIVITY_CANCELLED",
  "message": "活动报名已取消"
}
```

核心规则：

- 只能取消当前仍为 `CONFIRMED` 的报名记录。
- 取消成功后人数减少；如果活动原状态为 `FULL`，状态恢复为 `OPEN`。

## 场地预约接口

### GET `/api/rooms`

用途：查询可预约场地及当前活跃预约数量。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 场地 ID |
| `name` | string | 场地名称 |
| `building` | string | 所属楼宇 |
| `capacity` | number | 容纳人数 |
| `status` | string | `AVAILABLE` 或 `MAINTENANCE` |
| `activeReservations` | number | 待审核或已通过预约数量 |

### GET `/api/room-reservations?username=student01`

用途：查询当前用户的场地预约记录。

### POST `/api/rooms/{roomId}/reservations`

用途：提交场地预约申请，成功后生成待审核任务、通知和审计日志。

请求：

```json
{
  "username": "student02",
  "reservationDate": "2026-06-30",
  "startHour": 10,
  "endHour": 12
}
```

核心规则：

- 场地必须存在且状态为 `AVAILABLE`。
- 只能预约今天或未来日期。
- 预约时间必须在 8:00-22:00 内，且单次不超过 3 小时。
- 同一场地同一日期的重叠 `PENDING` / `APPROVED` 时段返回 `409`。

## 设备借用接口

### GET `/api/devices`

用途：查询可借用设备及库存状态。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 设备 ID |
| `name` | string | 设备名称 |
| `category` | string | 设备分类 |
| `totalQuantity` | number | 总数量 |
| `availableQuantity` | number | 可借数量 |
| `status` | string | `AVAILABLE` 或 `OUT_OF_STOCK` |

### GET `/api/device-borrows?username=student01`

用途：查询当前用户设备借用记录。

### POST `/api/devices/{deviceId}/borrow`

用途：提交设备借用申请，成功后生成待审核任务、通知和审计日志。

请求：

```json
{
  "username": "student02",
  "quantity": 1,
  "borrowedAt": "2026-06-30",
  "dueAt": "2026-07-07"
}
```

核心规则：

- 设备必须存在且状态为 `AVAILABLE`。
- 借用数量必须大于 0 且不能超过 `availableQuantity`。
- 借用开始日期不能晚于归还日期。
- 同一用户同一设备已有 `PENDING` 或 `BORROWED` 记录时返回 `409`。

## 消息通知接口

### GET `/api/notifications?username=student01`

用途：查询当前用户通知列表。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 通知 ID |
| `title` | string | 通知标题 |
| `readFlag` | boolean | 是否已读 |

### POST `/api/notifications/{notificationId}/read`

用途：标记本人通知为已读。

请求：

```json
{
  "username": "student01"
}
```

核心规则：

- 用户必须存在且状态为 `ACTIVE`。
- 只能标记属于当前用户的通知；跨用户通知返回 `404`。

## BookNest 接口

### GET `/api/books?keyword=测试`

用途：按书名、作者、分类或 ISBN 检索图书。`keyword` 为空时返回全部示例图书。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 图书 ID |
| `isbn` | string | 示例 ISBN |
| `title` | string | 书名 |
| `author` | string | 作者 |
| `category` | string | 分类 |
| `totalCopies` | number | 馆藏总数 |
| `availableCopies` | number | 可借数量 |

### GET `/api/book-borrows?username=student01`

用途：查询当前用户借阅记录。

核心规则：

- 用户必须存在且状态为 `ACTIVE`。
- 响应按借阅记录 ID 倒序返回。

### POST `/api/books/{bookId}/borrow`

用途：借阅图书。

请求：

```json
{
  "username": "student02"
}
```

成功响应：

```json
{
  "code": "BOOK_BORROWED",
  "message": "图书借阅成功"
}
```

核心规则：

- 图书必须存在。
- `availableCopies` 必须大于 0。
- 用户同时持有的 `BORROWED` 和 `OVERDUE` 图书不能超过 3 本。
- 借阅成功后生成 `BORROWED` 记录，应还日期为借阅日期后 30 天，可借数量减少 1。

### POST `/api/book-borrows/{borrowId}/renew`

用途：续借图书。

核心规则：

- 只能续借当前用户自己的借阅记录。
- 只有 `BORROWED` 状态可以续借。
- 每条记录最多续借 1 次。
- 逾期图书不能续借。
- 续借成功后应还日期延后 14 天。

### POST `/api/book-borrows/{borrowId}/return`

用途：归还图书。

核心规则：

- 只有 `BORROWED` 或 `OVERDUE` 状态可以归还。
- 归还成功后借阅记录变为 `RETURNED`，图书可借数量增加 1。

## 后台审核接口

### GET `/api/admin/review-tasks`

用途：查询审核任务。当前教学版本未接入登录态，接口用于展示审核列表和测试越权场景。

响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 审核任务 ID |
| `taskType` | string | 任务类型 |
| `title` | string | 任务标题 |
| `applicant` | string | 申请人 |
| `status` | string | `PENDING`、`APPROVED` 或 `REJECTED` |
| `reviewer` | string/null | 审核人 |
| `comment` | string/null | 审核备注 |
| `createdAt` | string | 创建时间 |
| `reviewedAt` | string/null | 审核时间 |

### POST `/api/admin/review-tasks/{taskId}/decision`

用途：处理审核任务。

请求：

```json
{
  "reviewer": "admin01",
  "decision": "APPROVED",
  "comment": "示例审核通过"
}
```

核心规则：

- 审核人必须是 `SYSTEM_ADMIN`、`LIBRARIAN` 或 `LOGISTICS_ADMIN`。
- `decision` 只能是 `APPROVED` 或 `REJECTED`。
- 只能处理 `PENDING` 任务。
- 处理成功后写入审核人、备注、审核时间和审计日志。

## Postman 对齐口径

Postman 集合路径：`test-assets/postman/campushub.postman_collection.json`。

集合应至少覆盖：

- 健康检查和项目概览。
- 学生登录成功、密码错误、锁定账号。
- 活动列表、报名成功、重复报名、满员报名、取消报名。
- 场地列表、预约记录、预约成功、维护中场地拒绝。
- 设备列表、设备借用记录、借用成功、无库存设备拒绝。
- 通知列表、标记本人通知为已读、跨用户通知拒绝。
- 图书检索、借阅记录、借阅成功、无库存借阅、续借成功、二次续借失败、归还。
- 审核任务列表、管理员审核成功、学生越权审核失败。

执行前建议重启后端，保证 H2 示例数据恢复到 `data.sql` 初始状态。
