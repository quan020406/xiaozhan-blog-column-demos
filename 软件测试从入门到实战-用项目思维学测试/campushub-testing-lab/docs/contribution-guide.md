# 贡献说明

CampusHub Testing Lab 是教学项目，欢迎围绕测试学习场景补充功能、用例和脚本。

## 本地开发

后端：

```powershell
cd backend
mvn spring-boot:run
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

质量检查：

```powershell
python scripts\check_release.py
```

## 提交前检查

- 不提交真实账号、手机号、邮箱、Token、Cookie。
- 不提交本机绝对路径或私有代理配置。
- 不提交 `target/`、`node_modules/`、`dist/`、日志和缓存文件。
- 新增测试脚本必须有 README 或运行说明。
- 性能测试内容只能提供脚本和报告模板，不能伪造性能结论。

## 推荐贡献方向

- 补充更多手工测试用例。
- 补充接口测试集合。
- 扩展 Selenium 流程。
- 扩展 JMeter 参数化脚本。
- 将场地预约和设备借用扩展为完整闭环。
