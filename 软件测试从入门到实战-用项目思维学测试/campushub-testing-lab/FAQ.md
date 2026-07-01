# FAQ

## 这个项目先启动什么？

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

后端默认是：

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
2. `http://localhost:8080/api/health` 是否正常返回。
3. 如果后端不是 `8080`，前端是否设置了 `VITE_API_BASE_URL`。
4. 修改环境变量后是否重启了前端 dev server。
5. 浏览器控制台里是否有接口跨域、代理或网络错误。

## 默认账号是什么？

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 学生 | `student01` | `campus123` |
| 学生 | `student02` | `campus123` |
| 管理员 | `admin01` | `campus123` |

这些账号都是虚拟教学数据。

## 为什么重启后数据会恢复？

项目默认使用 H2 内存数据库。应用启动时会重新加载 `schema.sql` 和 `data.sql`，保证每次练习都有一致的初始数据。

## 这个项目适合直接部署生产吗？

不适合。它是测试教学项目，登录、权限、数据规模和部署方式都按教学演示设计。博客中可以展示运行方式、测试思路和测试资产，不能把它描述成生产级系统。

## 为什么没有把 QA Command Center 作为首页？

当前版本优先让读者先操作普通业务页面，再理解测试如何介入业务交付。质量看板可以作为后续进阶视图，但不替代首页业务体验。

## 当前需要检查哪些测试资产？

基础材料：

- `docs/requirements.md`
- `docs/api-contract.md`
- `docs/data-dictionary.md`
- `docs/test-strategy.md`
- `test-assets/test-cases/core-cases.md`
- `test-assets/bug-reports/sample-activity-registration-full.md`
- `test-assets/postman/campushub.postman_collection.json`
- `test-assets/known-defects.md`

自动化和性能材料：

- `test-assets/selenium/test_login_activity_book.py`
- `test-assets/jmeter/campushub-activity-booknest-smoke.jmx`
- `scripts/run_performance_probe.py`
- `scripts/check_ui_smoke.py`

## 性能探针怎么跑？

先启动后端，再执行：

```powershell
python scripts\run_performance_probe.py --base-url http://localhost:8080 --loops 5
```

输出文件在 `test-assets/reports/`。它只用于第 23-26 期教学演示，不代表通用性能结论。
