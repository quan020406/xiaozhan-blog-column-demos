# 数据库设计

当前版本使用 H2 内存数据库，启动时执行：

- `backend/src/main/resources/schema.sql`
- `backend/src/main/resources/data.sql`

## 核心实体关系

```text
campus_user 1 -- n activity_registration n -- 1 activity
campus_user 1 -- n book_borrow n -- 1 book
campus_user 1 -- n notification
review_task 记录后台审核任务
audit_log 记录关键操作
room 和 device 为后续场地、设备审核案例提供基础数据
```

## 状态字段

| 表 | 字段 | 主要值 |
| --- | --- | --- |
| `campus_user` | `status` | `ACTIVE`, `LOCKED` |
| `activity` | `status` | `OPEN`, `FULL` |
| `activity_registration` | `status` | `CONFIRMED`, `CANCELLED` |
| `book_borrow` | `status` | `BORROWED`, `OVERDUE`, `RESERVED`, `RETURNED` |
| `review_task` | `status` | `PENDING`, `APPROVED`, `REJECTED` |

## 第一版测试关注点

- 活动报名成功后，`activity.registered_count` 应增加。
- 活动取消报名后，`activity.registered_count` 应减少。
- 图书借阅成功后，`book.available_copies` 应减少。
- 图书归还成功后，`book.available_copies` 应增加。
- 审核任务处理后，`review_task.status` 和 `reviewer` 应更新。
- 关键动作应写入 `audit_log`。
