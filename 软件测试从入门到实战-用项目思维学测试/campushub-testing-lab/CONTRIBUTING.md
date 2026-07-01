# 贡献指南

CampusHub Testing Lab 是面向软件测试学习的教学项目。贡献优先围绕“读者能否启动、能否操作、能否把业务现象转成测试产物”展开。

## 可贡献内容

- 修复登录、活动报名、BookNest、场地、设备、通知、审核相关问题。
- 补充明确的业务规则、边界条件和错误提示。
- 补充手工测试用例、Bug 报告、Postman 请求、Selenium 脚本或 JMeter 脚本。
- 改进 README、FAQ、学习路线、发布检查和测试策略说明。
- 修复发布检查、完成度检查、烟测或性能探针脚本中的问题。

## 暂缓内容

- 生产级认证、权限系统和部署方案。
- 真实第三方服务、真实学校数据和真实用户数据。
- 复杂质量大屏、营销式首页和与测试教学无关的视觉装饰。
- 未经验证的性能结论。

## 本地开发检查

后端：

```powershell
cd backend
mvn test
```

前端：

```powershell
cd frontend
npm run build
```

发布检查：

```powershell
python scripts\check_release.py
python scripts\check_completion.py
```

页面烟测需要先启动后端和前端：

```powershell
python scripts\check_ui_smoke.py --base-url http://127.0.0.1:5173
```

## 提交边界

- 不提交真实账号、手机号、邮箱、Token、Cookie、学校数据或个人隐私数据。
- 不提交本机绝对路径、私有代理、IDE 缓存、构建产物、日志和依赖目录。
- 新增接口必须同步 API 契约，并至少补一条测试覆盖。
- 新增业务规则必须同步需求说明、用例或已知缺陷文档。
- 新增测试资产必须能对应到页面、接口、PRD 需求或文章素材映射。
