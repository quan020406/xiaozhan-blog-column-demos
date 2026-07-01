import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pages import CampusHubPage


def parse_args():
    parser = argparse.ArgumentParser(description="CampusHub UI smoke test for Selenium articles.")
    parser.add_argument("--base-url", default="http://localhost:5173", help="CampusHub frontend URL.")
    parser.add_argument("--username", default="student02", help="Student username.")
    parser.add_argument("--password", default="campus123", help="Student password.")
    parser.add_argument("--output", default="test-assets/reports/selenium-latest.json", help="Output summary JSON.")
    return parser.parse_args()


def main():
    args = parse_args()
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 12)
    page = CampusHubPage(driver, wait)
    steps = []

    def record(name, status, detail):
        steps.append({"name": name, "status": status, "detail": detail})

    try:
        page.open(args.base_url)
        page.login(args.username, args.password)
        page.wait_for_action("register-activity")
        record("login", "passed", "学生账号登录成功")

        if not page.click_first_enabled("register-activity"):
            record("activity", "skipped", "当前示例数据没有可报名活动")
        else:
            page.wait_for_feedback()
            record("activity", "passed", "活动报名动作已执行并得到页面反馈")

        page.go_to_nav("图书列表")
        page.wait_for_action("borrow-book")
        if not page.click_first_enabled("borrow-book"):
            record("booknest", "skipped", "当前示例数据没有可借图书")
        else:
            page.wait_for_feedback()
            record("booknest", "passed", "BookNest 借阅动作已执行并得到页面反馈")

        status = "passed" if all(step["status"] in {"passed", "skipped"} for step in steps) else "failed"
    except Exception as exc:
        status = "failed"
        record("failure", "failed", str(exc))
        raise
    finally:
        driver.quit()
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                {
                    "runId": "ui-selenium-latest",
                    "status": status,
                    "generatedAt": datetime.now(timezone.utc).isoformat(),
                    "baseUrl": args.base_url,
                    "steps": steps,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
