# xiaozhan-blog-column-demos

这是小湛博客专栏配套 Demo 仓库，用来集中存放文章中涉及的示例工程、验证脚本、配套素材和运行说明。

每个专栏独立放在一个目录下，后续新增专栏或 Demo 时，直接新增同级目录，避免不同文章系列的代码和素材混在一起。

## 专栏目录

| 专栏 | 内容 | 入口 |
| --- | --- | --- |
| 下一代工作流：当 AI 成为我的全职下属 | Spring Boot 高并发秒杀 Demo、AI 工程治理脚本、配套运行素材 | [下一代工作流-当AI成为我的全职下属](./下一代工作流-当AI成为我的全职下属/) |
| 撕开黑盒学大模型：从白盒状态机演进到工业级 Agent 框架 | 纯 Python ReAct、记忆治理、ReWOO 异步调度、LangChain/LangGraph 对照骨架 | [撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架](./撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架/) |
| 软件测试从入门到实战：用项目思维学测试 | CampusHub 测试教学项目、文章草稿、测试素材、接口/UI/性能测试练习入口 | [软件测试从入门到实战-用项目思维学测试](./软件测试从入门到实战-用项目思维学测试/) |

## 静态动画页

| 主题 | 页面 | iframe 示例 |
| --- | --- | --- |
| 第三期：AI Agent 防作弊 CI | [第三期动画辅助理解](./animations/article-03/) | [iframe-snippets.md](./animations/article-03/iframe-snippets.md) |

## 仓库约定

- 根目录只放仓库总览、通用配置和各专栏目录。
- 每个专栏目录保留自己的 `README.md`，说明 Demo 运行方式和注意事项。
- 本机环境变量、私有地址、端口和密钥不提交到仓库；只提交 `.env.example` 这类示例配置。
- Java、Python 等构建产物不提交，例如 `target/`、`__pycache__/`、`.pytest_cache/`。

## 只拉取某个目录

如果只想下载某个专栏或某个 Demo，可以使用 Git sparse-checkout：

```powershell
git clone --filter=blob:none --sparse git@github.com:quan020406/xiaozhan-blog-column-demos.git
cd xiaozhan-blog-column-demos
git sparse-checkout set "下一代工作流-当AI成为我的全职下属/demo/AutoEnterprise-Seckill"
```

如果后续想切换到另一个目录，重新执行 `git sparse-checkout set "<目标目录>"` 即可。

## 当前可用 Demo

### Mini Agent Lab

位置：[撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架](./撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架/)

这是一个面向 LLM Agent 底层机制拆解的 Python 示例工程，用于演示：

- 纯 Python ReAct 状态机与函数自省工具注册
- 长短期记忆分层治理与相似度阈值过滤
- 简化版 ReWOO / DAG 异步并发调度
- 手写实现到 LangChain / LangGraph 的迁移映射

运行前请进入 `撕开黑盒学大模型-从白盒状态机演进到工业级Agent框架` 查看专栏 README。

### AutoEnterprise-Seckill

位置：[下一代工作流-当AI成为我的全职下属/demo/AutoEnterprise-Seckill](./下一代工作流-当AI成为我的全职下属/demo/AutoEnterprise-Seckill/)

这是一个 Spring Boot + MyBatis-Plus + H2 + Redisson 的高并发秒杀 Demo，用于演示：

- 先查后改导致的超卖风险
- 数据库条件更新的原子扣减方案
- Redisson 分布式锁模式
- 面向 AI Agent 的上下文裁剪、提交审计和防作弊检查

运行前请进入对应 Demo 目录查看专栏 README 和 Demo README。

### CampusHub Testing Lab

位置：[软件测试从入门到实战-用项目思维学测试/campushub-testing-lab](./软件测试从入门到实战-用项目思维学测试/campushub-testing-lab/)

这是一个面向软件测试学习路径的 Spring Boot + Vue 教学项目，用于演示：

- CampusHub 校园服务协作平台的需求、数据字典和接口契约
- 登录、活动报名、BookNest 图书借阅和后台审核等测试场景
- 手工测试用例、Bug 报告、Postman、Selenium 和 JMeter 示例素材
- 面向专栏文章的结构检查、发布检查和项目化学习路线

运行前请进入 `软件测试从入门到实战-用项目思维学测试` 查看专栏 README，再进入 `campushub-testing-lab` 查看工程启动说明。
