# 贡献指南

CampusHub Testing Lab 是面向软件测试学习的教学项目。贡献内容应优先服务测试对象、测试素材和可复现练习，不追求业务系统复杂度。

## 可贡献内容

- 补充 CampusHub 业务规则、测试点和异常场景。
- 补充手工测试用例、Bug 报告样例、Postman 集合、Selenium 脚本或 JMeter 脚本。
- 修复后端接口、前端演示页面、QA Console 看板数据生成脚本中的问题。
- 改进 README、FAQ、学习路线和发布前检查说明。

## 本地开发检查

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```

涉及自动化证据时，建议额外执行：

```powershell
python test-assets\selenium\test_login_activity_book.py --base-url http://127.0.0.1:5173
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
python scripts\generate_test_dashboard.py
```

## 提交边界

- 不提交真实账号、手机号、邮箱、Token、Cookie、学校数据或个人隐私数据。
- 不提交本机绝对路径、私有代理、IDE 缓存、构建产物、日志和依赖目录。
- 性能测试结果只作为本机样例证据，不能写成通用性能结论。
- 新增脚本必须包含运行说明，新增接口必须同步 API 契约和至少一条测试覆盖。

