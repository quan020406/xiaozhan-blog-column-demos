# Selenium 示例脚本

## 用途

`test_login_activity_book.py` 演示一个稳定核心流程：

1. 打开 CampusHub 前端。
2. 使用学生账号登录。
3. 报名一个开放活动。
4. 借阅一本可借图书。

## 环境要求

- Python 3.10+
- Chrome 浏览器
- Selenium 4.6+，使用 Selenium Manager 自动解析驱动

安装依赖：

```powershell
pip install -r requirements.txt
```

运行前先启动项目：

```powershell
cd backend
mvn spring-boot:run

cd ..\frontend
npm run dev
```

运行脚本：

```powershell
python test_login_activity_book.py --base-url http://localhost:5173
```

如验证失败，脚本会在当前目录生成 `selenium-failure.png`。
