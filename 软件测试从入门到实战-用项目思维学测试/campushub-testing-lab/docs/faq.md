# 常见问题

## 1. 为什么登录返回的是 demo token？

这是教学项目第一版，目标是支撑测试流程、测试设计和自动化脚本练习。当前 token 只用于演示登录成功后的返回结构，不作为生产安全方案。

## 2. H2 数据会持久保存吗？

不会。默认使用 H2 内存库，应用重启后会重新加载 `schema.sql` 和 `data.sql`。这能保证读者每次练习都有一致的初始数据。

## 3. 8080 端口被占用怎么办？

可以改端口启动后端：

```powershell
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=18080"
```

然后前端启动前设置：

```powershell
$env:VITE_API_BASE_URL="http://localhost:18080"
npm run dev
```

## 4. Selenium 脚本需要固定浏览器驱动吗？

脚本使用 Selenium 4，优先依赖 Selenium Manager 自动解析驱动。读者仍需安装本机 Chrome 浏览器。

## 5. JMeter 脚本能证明系统性能吗？

不能。当前 `.jmx` 只是性能测试入门脚本，帮助读者学习参数化和接口压测入口。性能结论必须由读者在自己的机器上实际运行后填写，不能直接套用。

## 6. 可以接入 MySQL 吗？

可以作为后续扩展。第一版默认 H2 是为了降低启动门槛，保证专栏读者能先完成测试练习。
