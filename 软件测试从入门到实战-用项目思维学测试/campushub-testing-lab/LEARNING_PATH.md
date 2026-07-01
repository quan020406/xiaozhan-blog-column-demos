# 学习路线

CampusHub Testing Lab 按 01-26 期文章顺序组织内容。建议先完成一次业务操作，再阅读测试资产和脚本。

## 推荐顺序

| 阶段 | 学习主题 | CampusHub 入口 | 产出物 |
| --- | --- | --- | --- |
| 1 | 认识测试对象 | 登录、活动列表、图书列表、我的记录 | 功能清单、风险清单 |
| 2 | 需求分析 | 报名名额、重复报名、库存扣减、续借限制 | 需求评审问题列表 |
| 3 | 用例设计 | 登录校验、活动边界、BookNest 状态流转 | 手工测试用例表 |
| 4 | 缺陷管理 | 满员报名、重复借阅、权限入口 | Bug 报告样例 |
| 5 | 接口测试 | `/api/auth/login`、`/api/activities`、`/api/books`、`/api/book-borrows` | Postman 集合 |
| 6 | 测试分类与发布策略 | 全业务主链路 | 发布检查清单 |
| 7 | UI 自动化 | 登录、活动、BookNest | Selenium 脚本 |
| 8 | 性能测试入门 | 活动列表、图书搜索、登录后报名链路 | JMeter 脚本、性能探针 |

## 读者操作路径

1. 按 `README.md` 启动后端和前端。
2. 使用 `student01 / campus123` 登录。
3. 完成一次活动报名和一次 BookNest 图书借阅。
4. 在“我的记录”确认业务数据变化。
5. 阅读 `docs/requirements.md`，把页面现象还原成需求规则。
6. 阅读 `test-assets/test-cases/core-cases.md`，把规则转成测试用例。
7. 阅读 `test-assets/bug-reports/sample-activity-registration-full.md`，学习 Bug 报告结构。
8. 导入 `test-assets/postman/campushub.postman_collection.json`，观察成功和失败返回。
9. 到第 20-22 期再运行 Selenium。
10. 到第 25-26 期再运行 JMeter 或性能探针。

## 文章与素材对应

完整对应关系见：

```text
test-assets/article-evidence-map.md
```

其中 `test-assets/article-deliverables/03-24-method-tables.md` 提供部分文章可直接复用的方法表、判定表和检查清单。
