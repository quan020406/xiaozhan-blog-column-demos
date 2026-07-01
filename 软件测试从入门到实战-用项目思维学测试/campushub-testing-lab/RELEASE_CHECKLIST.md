# 发布前检查清单

本文档用于确认 CampusHub Testing Lab 是否适合放到 GitHub 公共仓库和博客文章中展示。

## 1. 启动检查

后端：

```powershell
cd backend
mvn spring-boot:run
```

确认：

```text
http://localhost:8080/api/health
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

确认：

```text
http://localhost:5173
```

如果后端端口不是 `8080`，前端启动前设置：

```powershell
$env:VITE_API_BASE_URL="http://localhost:18080"
```

## 2. 业务页面检查

- 使用 `student01 / campus123` 登录成功。
- 活动列表可加载，开放活动可以报名，满员或关闭活动不能报名。
- 图书列表可加载，关键词检索可用，有库存图书可以借阅。
- 场地预约可提交可用场地，维护场地和冲突时段会被拒绝。
- 设备借用可提交有库存设备，库存不足或重复申请会被拒绝。
- 消息通知可展示并标记已读。
- “我的记录”能看到当前账号的报名、借阅、预约和设备借用记录。
- 使用 `admin01 / campus123` 登录后，“管理员入口”展示统计、库存、异常样例和审核任务。
- “测试素材”能引导到需求、用例、Bug、接口、Selenium、JMeter 和文章追踪。

## 3. 基础资产检查

必须存在：

- `docs/requirements.md`
- `docs/api-contract.md`
- `docs/data-dictionary.md`
- `docs/test-strategy.md`
- `test-assets/test-cases/core-cases.md`
- `test-assets/bug-reports/sample-activity-registration-full.md`
- `test-assets/postman/campushub.postman_collection.json`
- `test-assets/known-defects.md`
- `test-assets/article-evidence-map.md`
- `test-assets/article-deliverables/03-24-method-tables.md`
- `test-assets/selenium/pages.py`
- `test-assets/selenium/test_login_activity_book.py`
- `test-assets/jmeter/campushub-activity-booknest-smoke.jmx`
- `scripts/run_performance_probe.py`
- `scripts/check_ui_smoke.py`

## 4. 构建和测试

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
python scripts\check_completion.py
```

可选页面烟测：

```powershell
python scripts\check_ui_smoke.py --base-url http://127.0.0.1:5173
```

执行前需要后端和前端都已启动。

可选性能探针：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

## 5. 公共仓库边界

- README、FAQ、学习路线、贡献指南和发布检查必须能独立解释项目如何启动、如何使用、如何验证。
- 不包含真实账号、真实手机号、真实邮箱、密钥、Cookie、Token 或私有代理。
- 不包含本机绝对路径。
- 不提交 `node_modules/`、`dist/`、`target/`、日志、缓存和 `test-assets/reports/`。
- Selenium、JMeter 和性能探针是教学练习，不写成通用性能承诺。
- 博客正文、写作规划和封面配图保留在本地写作区，不作为公开仓库必要内容。
