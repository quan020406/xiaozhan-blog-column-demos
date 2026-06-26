# 第一版测试策略

## 测试目标

验证 CampusHub Testing Lab 第一版是否满足教学项目的基本可用性：

- 普通学生可登录、报名活动、借阅图书。
- 图书借阅支持续借和归还。
- 管理员可处理基础审核任务。
- 示例数据、测试素材和脚本可用于专栏文章讲解。

## 测试层级

| 层级 | 范围 | 入口 |
| --- | --- | --- |
| 后端构建 | Java 编译和 Spring Boot 依赖 | `mvn test` |
| 前端构建 | TypeScript 类型检查和 Vite 构建 | `npm run build` |
| 接口烟测 | 登录、报名、借阅、审核核心接口 | Postman 或 PowerShell |
| 手工测试 | 页面端到端流程 | `test-assets/test-cases/` |
| UI 自动化 | 登录、报名、借阅核心流程 | `test-assets/selenium/` |
| 性能入口 | 活动列表和图书检索读取接口 | `test-assets/jmeter/` |
| 发布检查 | 结构、敏感信息、本机路径、JMeter XML | `python scripts/check_release.py` |

## 不做的事

- 不给出通用性能结论。
- 不接入真实短信、邮件、支付或统一身份认证。
- 不使用真实学校、真实用户或真实联系方式。
- 不把演示登录方案描述为生产安全方案。

## 验收命令

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```
