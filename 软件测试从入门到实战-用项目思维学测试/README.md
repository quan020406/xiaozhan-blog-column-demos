# 软件测试从入门到实战：用项目思维学测试

这是一个面向测试新人、转岗学习者和校招实习准备者的测试专栏项目。专栏不复用课程课件中的原始案例，而是统一使用原创贯穿项目来讲解软件测试知识。

当前贯穿项目已确定为 **CampusHub 校园服务协作平台 + 内置 BookNest 图书借阅模块**。后续文章、用例模板、Demo、自动化脚本和性能素材都围绕这条主线推进。

如果你只想运行博客示范项目，直接进入：

```text
campushub-testing-lab/
```

入口文档：

- [CampusHub Testing Lab](./campushub-testing-lab/README.md)
- [学习路线](./campushub-testing-lab/LEARNING_PATH.md)
- [常见问题](./campushub-testing-lab/FAQ.md)

## 专栏定位

- 目标读者：零基础测试学习者、准备测试岗位面试的学生、希望补齐测试体系的开发者。
- 写作方式：每篇文章围绕一个项目问题展开，用测试思维拆解，再给出清单、模板或可复用方法。
- 内容范围：测试基础、需求分析、缺陷管理、测试用例设计、测试分类、Web 自动化、性能测试和 JMeter 入门。
- 案例边界：所有案例围绕 CampusHub 重新设计，不照搬课件中的生活类比、网站示例、邮箱注册、搜索引擎、博客系统或汽车性能类比。

## 目录结构

```text
articles/                   # 本地可发布文章草稿和正式正文，不上传 GitHub
assets/images/              # 本地专栏封面、文章配图和可视化素材，不上传 GitHub
case-project/               # 贯穿项目设定、历史候选记录、需求池和测试素材
campushub-testing-lab/       # 可运行的博客配套示范项目
docs/                       # 本地专栏规划、发布检查和写作说明，不上传 GitHub
scripts/                    # 专栏结构、禁用案例和可移植性检查脚本
templates/                  # 后续文章统一模板
```

## 贯穿项目

CampusHub 覆盖账号登录、活动报名、场地预约、设备借用、消息通知和后台审核等模块。BookNest 作为 CampusHub 内置图书借阅模块，重点承载等价类、边界值、判定表、状态流转和数据一致性等用例设计内容。

示范项目已经提供：

- Spring Boot 后端、Vue 前端、H2 示例数据。
- Swagger/OpenAPI、Postman 集合。
- 手工测试用例、Bug 报告样例。
- Selenium UI 自动化脚本和截图证据。
- JMeter 脚本、性能探针和 QA Command Center 看板。

## 发布路线

| 阶段 | 文章范围 | 目标 |
| --- | --- | --- |
| 第一阶段 | 01-08 | 建立测试认知，理解需求、流程和缺陷管理 |
| 第二阶段 | 09-15 | 掌握测试用例设计方法，并能输出结构化用例 |
| 第三阶段 | 16-18 | 梳理测试分类和版本发布前的测试策略 |
| 第四阶段 | 19-22 | 从手工测试过渡到 Selenium Web 自动化 |
| 第五阶段 | 23-26 | 入门性能测试指标、测试类型和 JMeter |

## 当前初始化内容

- [CampusHub Testing Lab](./campushub-testing-lab/README.md)
- [结构检查脚本](./scripts/check_column.py)
- [文章统一模板](./templates/article-template.md)

## 写作约定

- 每篇文章都从 CampusHub 的一个具体功能或质量问题切入。
- 概念解释不堆定义，优先回答“为什么需要这个测试动作”。
- 每篇至少保留一个可复制的表格、清单或模板。
- 不写无法验证的夸张结论，不伪造工具执行结果、性能数据或截图。
- 后续如补充 Demo，代码、数据和文章草稿应分目录存放，避免混在根目录。
