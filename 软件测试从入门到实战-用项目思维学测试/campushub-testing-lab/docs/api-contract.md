# API 契约

默认后端地址：`http://localhost:8080`

所有接口使用 JSON。当前版本是教学项目，登录返回演示 token，不作为生产鉴权方案。

## 通用错误

| 状态码 | 场景 |
| --- | --- |
| 400 | 请求参数不合法 |
| 401 | 用户名或密码错误 |
| 403 | 账号锁定或角色无权限 |
| 404 | 资源不存在 |
| 409 | 业务规则冲突，例如重复报名、无库存、不可续借 |

## 账号

### POST `/api/auth/login`

请求：

```json
{
  "username": "student01",
  "password": "campus123"
}
```

响应：

```json
{
  "token": "demo-token-student01",
  "user": {
    "id": 1,
    "username": "student01",
    "displayName": "测试学生一号",
    "roleCode": "STUDENT",
    "status": "ACTIVE"
  },
  "permissions": ["ACTIVITY_READ", "ACTIVITY_REGISTER", "BOOK_READ", "BOOK_BORROW"]
}
```

## 活动

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/activities?username=student01` | 查询活动列表，并标记当前用户是否已报名 |
| POST | `/api/activities/{activityId}/registrations` | 报名活动 |
| DELETE | `/api/activities/{activityId}/registrations/{username}` | 取消报名 |

报名请求：

```json
{
  "username": "student01"
}
```

## BookNest

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/books?keyword=test` | 检索图书 |
| GET | `/api/book-borrows?username=student01` | 查询我的借阅 |
| POST | `/api/books/{bookId}/borrow` | 借阅图书 |
| POST | `/api/book-borrows/{borrowId}/renew` | 续借图书 |
| POST | `/api/book-borrows/{borrowId}/return` | 归还图书 |

借阅、续借、归还请求：

```json
{
  "username": "student01"
}
```

核心规则：

- 可借数量为 0 时不能借阅。
- 每个用户最多同时持有 3 本 `BORROWED` 或 `OVERDUE` 图书。
- 每条借阅记录最多续借 1 次。
- 只有 `BORROWED` 或 `OVERDUE` 记录可以归还。

## 后台审核

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/admin/review-tasks` | 查询审核任务 |
| POST | `/api/admin/review-tasks/{taskId}/decision` | 处理审核任务 |

审核请求：

```json
{
  "reviewer": "admin01",
  "decision": "APPROVED",
  "comment": "示例审核通过"
}
```

审核人角色必须是 `SYSTEM_ADMIN`、`LIBRARIAN` 或 `LOGISTICS_ADMIN`。
