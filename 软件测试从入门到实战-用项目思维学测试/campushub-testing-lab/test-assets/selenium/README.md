# Selenium 示例脚本

本目录承接第 20-22 期文章。脚本只覆盖稳定主链路，不替代探索式测试。

## 运行前提

1. 后端已启动：`http://localhost:8080`
2. 前端已启动：`http://localhost:5173`
3. 本机安装 Chrome

## 安装依赖

```powershell
pip install -r test-assets\selenium\requirements.txt
```

## 执行

```powershell
python test-assets\selenium\test_login_activity_book.py --base-url http://127.0.0.1:5173
```

脚本会验证登录、活动列表、活动报名和 BookNest 借阅基础路径。失败时会在命令行输出失败步骤。

`pages.py` 提供最小页面对象分层：打开页面、登录、导航、点击首个可用按钮、等待反馈。第 22 期文章可以用它说明“手工步骤到脚本”的拆分方式，但不要把未运行截图写成真实执行证据。
