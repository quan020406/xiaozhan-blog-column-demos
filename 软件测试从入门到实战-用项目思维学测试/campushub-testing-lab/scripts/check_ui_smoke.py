from argparse import ArgumentParser
from datetime import datetime, timezone
import json
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


NAV_LABELS = ["活动列表", "图书列表", "场地预约", "设备借用", "消息通知", "我的记录", "管理员入口", "测试素材"]


def main() -> int:
    parser = ArgumentParser(description="CampusHub frontend smoke test.")
    parser.add_argument("--base-url", default="http://127.0.0.1:5173", help="Frontend URL.")
    parser.add_argument("--output", default="test-assets/reports/ui-smoke-latest.json", help="Output JSON path.")
    parser.add_argument("--username", default="student02", help="Student username.")
    parser.add_argument("--password", default="campus123", help="Student password.")
    args = parser.parse_args()

    steps: list[dict[str, str]] = []
    console_errors: list[str] = []

    def record(name: str, status: str, detail: str) -> None:
        steps.append({"name": name, "status": status, "detail": detail})

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        page.on("console", lambda msg: collect_console_error(msg, console_errors))
        try:
            page.goto(args.base_url, wait_until="networkidle")
            expect_text(page, "[data-testid='service-status']", "后端在线")
            record("load", "passed", "首页加载并显示后端在线")

            fill_login(page, args.username, args.password)
            expect_text(page, "[data-testid='success-message']", "登录成功")
            record("student-login", "passed", "学生账号登录成功")

            for label in NAV_LABELS:
                click_nav(page, label)
                record(f"nav-{label}", "passed", f"已进入{label}")

            click_nav(page, "活动列表")
            click_optional_action(page, "register-activity", "activity-register", record)

            click_nav(page, "图书列表")
            page.locator("[data-testid='book-search']").click()
            click_optional_action(page, "borrow-book", "book-borrow", record)

            click_nav(page, "场地预约")
            click_optional_action(page, "reserve-room", "room-reserve", record)

            click_nav(page, "设备借用")
            click_optional_action(page, "borrow-device", "device-borrow", record)

            page.locator("[data-testid='login-admin']").click()
            expect_text(page, "[data-testid='success-message']", "登录成功")
            click_nav(page, "管理员入口")
            page.get_by_role("heading", name="审核任务").wait_for(timeout=8_000)
            record("admin-entry", "passed", "管理员入口和审核任务区域可见")
        except Exception as exc:
            record("failure", "failed", str(exc))
        finally:
            browser.close()

    status = "passed" if all(step["status"] in {"passed", "skipped"} for step in steps) and not console_errors else "failed"
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "status": status,
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "baseUrl": args.base_url,
                "steps": steps,
                "consoleErrors": console_errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"ui smoke {status} output={output}")
    return 0 if status == "passed" else 1


def fill_login(page, username: str, password: str) -> None:
    page.locator("[data-testid='login-username']").fill(username)
    page.locator("[data-testid='login-password']").fill(password)
    page.locator("[data-testid='login-submit']").click()


def click_nav(page, label: str) -> None:
    page.get_by_role("button", name=label).click()
    page.get_by_text(label).first.wait_for(timeout=8_000)


def click_optional_action(page, test_id: str, name: str, record) -> None:
    buttons = page.locator(f"[data-testid='{test_id}']")
    for index in range(buttons.count()):
        button = buttons.nth(index)
        if button.is_enabled():
            button.click()
            wait_for_feedback(page)
            record(name, "passed", f"{test_id} 已执行并得到页面反馈")
            return
    record(name, "skipped", f"当前数据没有可执行的 {test_id} 按钮")


def wait_for_feedback(page) -> None:
    try:
        page.locator("[data-testid='success-message'], [data-testid='error-message']").wait_for(timeout=8_000)
    except PlaywrightTimeoutError:
        raise AssertionError("操作后未出现页面反馈")


def expect_text(page, selector: str, text: str) -> None:
    page.locator(selector).filter(has_text=text).wait_for(timeout=12_000)


def collect_console_error(msg, console_errors: list[str]) -> None:
    if msg.type != "error":
        return
    if msg.text.startswith("Failed to load resource:"):
        return
    console_errors.append(msg.text)


if __name__ == "__main__":
    raise SystemExit(main())
