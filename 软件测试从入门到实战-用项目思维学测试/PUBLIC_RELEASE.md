# 公开发布核对

本文档用于在上级多专栏仓库上传 GitHub 公共仓库前确认本专栏目录的发布边界。它不替代测试报告，只作为提交前检查清单。

## 应公开的内容

- `campushub-testing-lab/backend/`：Spring Boot 后端示例。
- `campushub-testing-lab/frontend/`：Vue 前端示例。
- `campushub-testing-lab/docs/`：工程需求、接口、数据字典和测试策略说明。
- `campushub-testing-lab/test-assets/`：测试用例、Bug 报告、Postman、Selenium、JMeter 和文章素材映射。
- `campushub-testing-lab/scripts/`：环境检查、发布检查、完成度检查、烟测和性能探针脚本。
- 本专栏目录内的 `README.md`、`.gitignore`、`PUBLIC_RELEASE.md`、`case-project/`、`scripts/`、`templates/`。
- 上级仓库根目录的 `README.md` 和 `.gitignore`，用于把本专栏加入公共仓库入口并放行工程文档。

## 不应公开的内容

- 本专栏目录内的 `articles/`：本地文章草稿和正式正文。
- 本专栏目录内的 `docs/`：本地专栏规划、发布检查和写作说明。
- 本专栏目录内的 `assets/images/`：本地封面、配图和截图素材。
- `campushub-testing-lab/test-assets/reports/`：本机运行生成的烟测、性能探针和临时报告。
- 任何 `.env`、Token、Cookie、真实账号、真实手机号、真实邮箱、真实学校数据、本机绝对路径或私有代理配置。

## 提交前命令

在本专栏目录执行：

```powershell
python scripts\check_column.py
```

在 `campushub-testing-lab/` 中执行：

```powershell
python scripts\check_release.py
python scripts\check_completion.py
```

后端测试：

```powershell
cd campushub-testing-lab\backend
mvn test
```

前端构建：

```powershell
cd campushub-testing-lab\frontend
npm run build
```

运行态烟测需要先启动后端和前端，再执行：

```powershell
cd campushub-testing-lab
python scripts\check_ui_smoke.py --base-url http://127.0.0.1:5173
```

## Git 提交核对

在上级仓库根目录提交前查看变更：

```powershell
git status --short
```

如果当前目录作为上级多专栏仓库的一部分发布，需要确认根目录 `.gitignore` 已经放行：

```text
软件测试从入门到实战-用项目思维学测试/campushub-testing-lab/docs/
```

同时仍要保持以下目录被忽略：

```text
软件测试从入门到实战-用项目思维学测试/articles/
软件测试从入门到实战-用项目思维学测试/docs/
软件测试从入门到实战-用项目思维学测试/assets/images/
```
