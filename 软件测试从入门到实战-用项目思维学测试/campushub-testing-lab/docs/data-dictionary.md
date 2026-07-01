# CampusHub 第一阶段数据字典

本文档记录第一阶段 H2 示例库的核心表结构。字段设计以测试教学为目标，优先保证可读性和后续案例扩展。

## campus_user

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| username | varchar(40) | 登录名 | 等价类、唯一约束 |
| display_name | varchar(80) | 页面显示名 | 长度边界、脱敏展示 |
| role_code | varchar(40) | 角色编码 | 权限矩阵 |
| password_hint | varchar(40) | 教学提示字段 | 后续替换为测试认证策略 |
| status | varchar(20) | 账号状态 | 正常、锁定等状态流转 |
| failed_login_count | int | 连续登录失败次数 | 登录锁定边界 |

## activity

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| title | varchar(120) | 活动名称 | 关键词搜索、长度边界 |
| organizer | varchar(80) | 组织方 | 筛选和权限 |
| location | varchar(80) | 活动地点 | 页面展示 |
| capacity | int | 名额上限 | 边界值 |
| registered_count | int | 已报名人数 | 满员判定 |
| status | varchar(20) | 活动状态 | 可报名、满员、关闭 |

## activity_registration

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| activity_id | bigint | 活动 ID | 关联完整性 |
| user_id | bigint | 用户 ID | 重复报名 |
| status | varchar(20) | 报名状态 | 报名、取消 |
| created_at | timestamp | 创建时间 | 截止时间边界 |

## book

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| isbn | varchar(30) | 图书编号 | 唯一约束 |
| title | varchar(120) | 书名 | 检索 |
| author | varchar(80) | 作者 | 检索 |
| category | varchar(60) | 分类 | 筛选 |
| total_copies | int | 馆藏总数 | 库存边界 |
| available_copies | int | 可借数量 | 借阅一致性 |

## book_borrow

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| book_id | bigint | 图书 ID | 关联完整性 |
| user_id | bigint | 用户 ID | 借阅数量上限 |
| status | varchar(20) | 借阅状态 | 借出、预约、逾期、归还 |
| borrowed_at | date | 借出日期 | 日期边界 |
| due_at | date | 应还日期 | 逾期判定 |
| renew_count | int | 续借次数 | 续借次数边界 |

## room

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| name | varchar(80) | 场地名称 | 检索展示 |
| building | varchar(80) | 所在楼栋 | 筛选 |
| capacity | int | 容量 | 预约适配 |
| status | varchar(20) | 场地状态 | 可用、维护 |

## device

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| name | varchar(80) | 设备名称 | 检索展示 |
| category | varchar(40) | 设备分类 | 筛选 |
| total_quantity | int | 总数量 | 库存边界 |
| available_quantity | int | 可借数量 | 库存一致性 |
| status | varchar(20) | 设备状态 | 缺货、可用 |

## notification

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| user_id | bigint | 用户 ID | 用户隔离 |
| title | varchar(120) | 通知标题 | 触达内容 |
| read_flag | boolean | 是否已读 | 状态切换 |

## review_task

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| task_type | varchar(40) | 审核类型 | 任务分类 |
| title | varchar(120) | 审核标题 | 页面展示 |
| applicant | varchar(40) | 申请人用户名 | 申请人追踪 |
| status | varchar(20) | 审核状态 | 待审、通过、驳回 |
| reviewer | varchar(40) | 审核人用户名 | 权限和审计 |
| comment | varchar(200) | 审核意见 | 驳回原因 |
| created_at | timestamp | 创建时间 | 排序和超时 |
| reviewed_at | timestamp | 审核时间 | 状态流转 |

## audit_log

| 字段 | 类型 | 说明 | 测试关注点 |
| --- | --- | --- | --- |
| id | bigint | 主键 | 唯一性 |
| actor | varchar(40) | 操作人 | 审计证据 |
| action | varchar(80) | 操作类型 | 行为追踪 |
| target_type | varchar(40) | 目标类型 | 定位对象 |
| target_id | bigint | 目标 ID | 定位对象 |
| created_at | timestamp | 操作时间 | 时间排序 |
