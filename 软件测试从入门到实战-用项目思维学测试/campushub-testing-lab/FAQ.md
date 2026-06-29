# FAQ

## 这个项目应该先启动什么？

先启动后端，再启动前端。后端提供 `/api` 接口，前端通过 Vite 代理访问后端。

```powershell
cd backend
mvn spring-boot:run
```

```powershell
cd frontend
npm install
npm run dev
```

## 浏览器访问哪个地址？

默认访问：

```text
http://localhost:5173
```

后端接口默认是：

```text
http://localhost:8080
```

## 8080 端口被占用怎么办？

后端改用 18080：

```powershell
cd backend
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=18080"
```

前端启动前设置代理目标：

```powershell
cd frontend
$env:VITE_API_BASE_URL="http://localhost:18080"
npm run dev
```

## 页面提示接口请求失败怎么办？

按顺序检查：

1. 后端是否已启动。
2. `http://localhost:8080/api/health` 是否返回正常。
3. 如果后端不是 8080，前端是否设置了 `VITE_API_BASE_URL`。
4. 是否在修改环境变量后重启了前端 dev server。

## 为什么 H2 数据重启后会恢复？

项目默认使用 H2 内存数据库。应用启动时会重新加载 `schema.sql` 和 `data.sql`，这样每次练习都有一致的初始数据。

## 默认账号是什么？

常用账号：

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 学生 | `student01` | `campus123` |
| UI 自动化学生 | `student02` | `campus123` |
| 管理员 | `admin01` | `campus123` |

更多账号见 `README.md`。

## Selenium 脚本怎么跑？

先启动后端和前端，再执行：

```powershell
pip install -r test-assets\selenium\requirements.txt
python test-assets\selenium\test_login_activity_book.py --base-url http://127.0.0.1:5173
```

它会生成 UI 截图和 `test-assets/reports/selenium-latest.json`。

## 没有 JMeter 怎么刷新性能趋势？

可以使用内置性能探针：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
python scripts\generate_test_dashboard.py
```

刷新浏览器后，QA Command Center 会读取新的性能趋势。

## JMeter 或性能探针结果能作为性能结论吗？

不能。当前脚本只用于教学和看板证据生成。真实性能结论必须结合机器配置、数据量、并发模型和多次运行结果重新分析。
