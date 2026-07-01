# 软件测试从入门到实战：用项目思维学测试

这是《软件测试从入门到实战：用项目思维学测试》的公开配套项目。仓库中的核心可运行工程是 **CampusHub Testing Lab**：一个面向测试学习者的校园服务协作平台 Demo，用来承载需求分析、用例设计、缺陷管理、接口测试、Selenium UI 自动化和 JMeter 性能测试入门。

如果你是从博客文章跳转过来的，直接进入：

```text
campushub-testing-lab/
```

核心入口：

- [CampusHub Testing Lab 工程说明](./campushub-testing-lab/README.md)
- [学习路线](./campushub-testing-lab/LEARNING_PATH.md)
- [常见问题](./campushub-testing-lab/FAQ.md)
- [发布前检查清单](./campushub-testing-lab/RELEASE_CHECKLIST.md)
- [公开发布核对](./PUBLIC_RELEASE.md)

## 项目定位

CampusHub Testing Lab 不是生产级校园系统，而是一个教学型测试练习项目。它把测试知识放进统一业务场景里，让读者能先操作系统，再把页面、接口和数据变化转成测试产物。

当前项目覆盖：

- 登录与权限：学生、管理员两类账号。
- 活动报名：列表、报名、取消报名、容量和状态限制。
- BookNest 图书借阅：图书检索、借阅、续借、归还和库存变化。
- 场地预约：日期、时段冲突、维护场地和审核状态。
- 设备借用：库存、借用日期、归还日期和审核任务。
- 消息通知：业务反馈和已读状态。
- 管理员入口：统计、库存、异常样例和审核任务。
- 测试资产：需求、用例、Bug、Postman、Selenium、JMeter 和文章素材映射。

## 目录结构

```text
campushub-testing-lab/       # 可运行的博客配套示范项目
case-project/                # 贯穿项目设定与历史候选记录
scripts/                     # 专栏结构检查脚本
templates/                   # 文章模板，仅用于本地写作参考
PUBLIC_RELEASE.md            # 上传 GitHub 前的公开发布核对
README.md                    # 当前说明
```

本地写作材料默认不进入公共仓库：

```text
articles/                    # 本地文章草稿和正文
docs/                        # 本地专栏规划与写作说明
assets/images/               # 本地专栏封面和文章配图
```

这些目录用于写作，不是读者运行 Demo 的必要条件。

## 快速开始

进入工程目录：

```powershell
cd campushub-testing-lab
```

检查本机环境：

```powershell
python scripts\verify_local.py
```

启动后端：

```powershell
cd backend
mvn spring-boot:run
```

启动前端：

```powershell
cd frontend
npm install
npm run dev
```

浏览器访问：

```text
http://localhost:5173
```

示例账号：

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 学生 | `student01` | `campus123` |
| 学生 | `student02` | `campus123` |
| 管理员 | `admin01` | `campus123` |

## 验证命令

在 `campushub-testing-lab/` 中执行：

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
python scripts\check_completion.py
```

在本目录执行专栏结构检查：

```powershell
python scripts\check_column.py
```

如果需要运行页面烟测，请先启动后端和前端，然后在 `campushub-testing-lab/` 中执行：

```powershell
python scripts\check_ui_smoke.py --base-url http://127.0.0.1:5173
```

## 发布边界

- 示例账号、密码和数据均为虚拟教学数据。
- 不提交真实手机号、真实邮箱、Token、Cookie、学校数据或个人隐私。
- 不提交 `node_modules/`、`dist/`、`target/`、日志、运行报告和缓存目录。
- Selenium、JMeter 和性能探针用于教学练习，不代表通用性能结论。
- 博客文章中的截图、命令输出和性能数据必须来自真实运行，不能伪造。
