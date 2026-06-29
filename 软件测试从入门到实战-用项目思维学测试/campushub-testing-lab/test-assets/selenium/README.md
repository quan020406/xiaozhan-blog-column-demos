# Selenium 示例脚本

## 用途

`test_login_activity_book.py` 演示一个稳定核心流程，并把截图写入 QA Console 可读取目录：

1. 打开 CampusHub 前端。
2. 使用学生账号登录。
3. 报名一个开放活动。
4. 提交场地预约。
5. 提交设备借用申请。
6. 借阅一本可借图书。
7. 标记本人通知为已读。

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

默认输出：

```text
frontend/src/assets/test-assets/screenshots/selenium-login.png
frontend/src/assets/test-assets/screenshots/selenium-activity.png
frontend/src/assets/test-assets/screenshots/selenium-room.png
frontend/src/assets/test-assets/screenshots/selenium-device.png
frontend/src/assets/test-assets/screenshots/selenium-booknest.png
frontend/src/assets/test-assets/screenshots/selenium-notification.png
test-assets/reports/selenium-latest.json
```

如验证失败，脚本会生成 `frontend/src/assets/test-assets/screenshots/selenium-failure.png`，并在 `test-assets/reports/selenium-latest.json` 记录失败步骤。
