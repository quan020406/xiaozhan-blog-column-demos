# 01-26 文章与项目素材追踪

本文档用于确认每期文章都能落到 CampusHub Testing Lab 的页面、接口或测试资产上。它不是写作大纲，而是项目完成度追踪表。

| 期数 | 文章主题 | 项目入口 | 必备素材 | 当前状态 |
| --- | --- | --- | --- | --- |
| 01 | 软件测试到底在测什么 | 活动列表、我的记录 | `docs/requirements.md`、`test-assets/test-cases/core-cases.md` | 已有 |
| 02 | 测试岗位与能力路线 | 活动报名规则 | 角色协作对照可落在 README/文章中 | 已有基础 |
| 03 | 需求不是一句话 | 活动报名 | 需求澄清表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 04 | 测试介入时机 | 活动报名 | 测试介入时间线 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 05 | V 模型和 W 模型 | 活动报名 | 模型对照表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 06 | Bug 流转 | BookNest 库存 | Bug 报告样例 | 已有基础 |
| 07 | Bug 沟通 | 管理员入口权限 | 争议判断清单 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 08 | 测试用例是什么 | 活动报名 | 用例基础模板 | 已有 |
| 09 | 通用用例设计 | 登录 | 测试点拆解表 | 已有基础 |
| 10 | 等价类划分 | 登录 | 等价类表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 11 | 边界值分析 | 活动容量 | 边界值用例表 | 已有基础 |
| 12 | 判定表法 | 活动报名条件 | 判定表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 13 | 正交法 | 图书搜索 | 因素水平表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 14 | 场景法 | BookNest 借阅闭环 | 基本流与备选流 | 已有基础 |
| 15 | 探索式测试 | 活动、图书、通知 | 探索式测试清单 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 16 | 测试分类 | 全系统 | 测试分类速查表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 17 | 单元/集成/系统/验收 | BookNest 库存 | 阶段对照表、后端测试 | 已有基础 |
| 18 | 冒烟/回归/Alpha/Beta | 发布检查 | `RELEASE_CHECKLIST.md` | 已有基础 |
| 19 | 自动化适用性 | 登录、活动列表 | 自动化筛选表 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 20 | Selenium 入门 | 登录 | `test-assets/selenium/test_login_activity_book.py` | 已补基础 |
| 21 | Selenium 稳定性 | 活动列表 | Selenium 等待与定位示例 | 已补基础 |
| 22 | 手工用例到脚本 | 登录、活动、图书 | `test-assets/selenium/pages.py`、`test-assets/selenium/test_login_activity_book.py` | 已补基础 |
| 23 | 性能测试指标 | 活动列表接口 | `scripts/run_performance_probe.py` | 已补基础 |
| 24 | 负载/压力/稳定性/容量 | 报名接口 | 性能类型对照 | `test-assets/article-deliverables/03-24-method-tables.md` |
| 25 | JMeter 从 0 到 1 | 活动列表接口 | `test-assets/jmeter/campushub-activity-booknest-smoke.jmx` | 已补基础 |
| 26 | JMeter 进阶 | 登录后报名链路 | JMeter 登录态和断言设计 | 已补基础 |

## 验证边界

- 01-26 的基础素材已经具备项目入口。
- Selenium 已补页面对象分层；文章如需截图证据，必须来自本机真实运行。
- JMeter 已补登录态提取、基础列表请求和报名链路；正式性能结论仍需独立环境、数据规模和多轮结果支撑。
