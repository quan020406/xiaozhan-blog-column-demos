# 发布前检查清单

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

如果后端使用 18080，前端启动前执行：

```powershell
$env:VITE_API_BASE_URL="http://localhost:18080"
```

## 2. 自动化证据

先保持后端和前端运行，再执行：

```powershell
python test-assets\selenium\test_login_activity_book.py --base-url http://127.0.0.1:5173
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
python scripts\generate_test_dashboard.py
```

如果后端使用 18080：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:18080 --loops 5
```

检查输出：

- `test-assets/reports/selenium-latest.json`
- `test-assets/reports/jmeter-latest.jtl`
- `frontend/src/assets/test-assets/test-dashboard.json`
- `frontend/src/assets/test-assets/screenshots/selenium-login.png`
- `frontend/src/assets/test-assets/screenshots/selenium-activity.png`
- `frontend/src/assets/test-assets/screenshots/selenium-room.png`
- `frontend/src/assets/test-assets/screenshots/selenium-device.png`
- `frontend/src/assets/test-assets/screenshots/selenium-booknest.png`
- `frontend/src/assets/test-assets/screenshots/selenium-notification.png`

## 3. 构建和测试

```powershell
cd backend
mvn test

cd ..\frontend
npm run build

cd ..
python scripts\check_release.py
```

在专栏根目录执行：

```powershell
cd ..
python scripts\check_column.py
```

## 4. 内容边界

- README、FAQ、学习路线、贡献说明和发布检查必须能独立解释项目如何启动、如何使用、如何验证。
- 不包含真实账号、真实手机号、真实邮箱、密钥、Cookie、Token 或私有代理。
- 不包含本机绝对路径。
- `node_modules/`、`dist/`、`target/`、日志和缓存不进入发布内容。
- 性能数据只能描述为本机样例证据，不写成通用性能承诺。

## 5. 发布资料入口

- `README.md`
- `FAQ.md`
- `LEARNING_PATH.md`
- `CONTRIBUTING.md`
- `docs/api-contract.md`
- `docs/test-strategy.md`
- `test-assets/postman/campushub-testing-lab.postman_collection.json`
