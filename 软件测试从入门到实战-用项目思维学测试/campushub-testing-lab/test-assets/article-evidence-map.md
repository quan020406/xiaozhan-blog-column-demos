# 文章与测试素材绑定索引

本文档把第 03-08 期基础篇文章中的交付物绑定到 CampusHub Testing Lab 的实际素材，避免文章只讲概念而没有项目落点。

## 文章交付物映射

| 期数 | 文章主题 | 可复制交付物 | 当前素材落点 | 看板字段 |
| --- | --- | --- | --- | --- |
| 03 | 需求不是一句话 | 自习室预约需求澄清表 | `docs/requirements.md`、`backend/src/main/resources/data.sql` 中的 `room` 样例 | 后续进入 `modules`、`testCases` |
| 04 | 测试介入时机 | 功能上线测试活动时间线 | `docs/test-strategy.md` | `runEvidence`、`bugs`、`testCases` |
| 05 | V 模型和 W 模型 | 模型与项目阶段对照表 | `docs/api-contract.md`、`docs/test-strategy.md` | `runEvidence` |
| 06 | Bug 流转 | Bug 单模板和状态流转表 | `test-assets/bug-reports/sample-book-inventory-inconsistency.md` | `bugs` |
| 07 | Bug 沟通 | Bug 争议沟通判断清单 | Bug 报告样例、看板风险队列 | `bugs`、`summary.qualityReason` |
| 08 | 测试用例 | 设备借用用例基础模板 | `test-assets/test-cases/activity-and-booknest-core-cases.md` | `testCases` |

## 第 03 期：需求澄清表示例

| 字段 | 内容 |
| --- | --- |
| 原始需求 | 学生要能预约自习室 |
| 涉及角色 | 学生、后勤管理员 |
| 正常流程 | 查询空闲时段，提交预约，管理员审核通过，学生收到通知 |
| 业务规则 | 仅预约未来 7 天；单次不超过 3 小时；维护中场地不可预约 |
| 异常场景 | 时间冲突、场地维护、超出时长、重复提交 |
| 数据变化 | 新增预约记录，审核状态变化，通知生成 |
| 待确认人 | 产品、后勤管理员、开发负责人 |
| 验收口径 | 页面提示、接口返回、状态写入和通知记录一致 |

## 第 06 期：Bug 单模板

| 字段 | 填写要求 |
| --- | --- |
| Bug 编号 | 使用 `CH-BUG-序号` 或模块前缀 |
| 标题 | 模块 + 操作 + 错误表现 |
| 严重程度 | Critical / Major / Minor |
| 优先级 | P0 / P1 / P2 |
| 发现版本 | 示例：`0.2.0-SNAPSHOT` |
| 模块 | 账号、活动、BookNest、后台审核、场地、设备 |
| 环境 | 后端、前端、浏览器、数据库 |
| 前置条件 | 账号、数据状态、启动条件 |
| 复现步骤 | 可由他人照做 |
| 期望结果 | 可判断的正确行为 |
| 实际结果 | 实际观察到的错误行为 |
| 附件或证据 | 截图、日志、接口响应、看板路径 |

## 第 08 期：用例基础模板

| 用例编号 | 标题 | 前置条件 | 步骤 | 预期结果 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| CH-DEV-001 | 借用有库存设备 | 用户已登录；设备可用数量大于 0 | 1. 打开设备借用；2. 选择设备；3. 提交申请 | 生成待审核申请，页面提示提交成功 | P0 |
| CH-DEV-002 | 库存为 0 的设备不可借用 | 设备状态为 `OUT_OF_STOCK` | 1. 打开设备列表；2. 查看操作按钮 | 借用按钮不可用，提示库存不足 | P1 |
| CH-DEV-003 | 重复申请同一设备被拦截 | 已有同一设备待审核申请 | 1. 再次选择同一设备；2. 提交申请 | 系统拒绝重复申请并说明原因 | P1 |

## 看板数据绑定

当前 `frontend/src/assets/test-assets/test-dashboard.json` 为 `sample` 模式：

- `testCases` 展示代表性用例，不等同全部 42 条聚合用例。
- `bugs` 展示开放风险队列样例。
- `runEvidence.commands` 展示命令证据。
- `automation.screenshots` 使用占位图，后续由 Selenium 覆盖。
- 阶段 8 的 `generate_test_dashboard.py` 应把 JUnit XML、Selenium 截图、JMeter `.jtl` 和 Bug Markdown 转成同一份 JSON。
