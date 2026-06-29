import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="CampusHub UI smoke test with screenshot evidence.")
    parser.add_argument("--base-url", default="http://localhost:5173", help="CampusHub frontend URL.")
    parser.add_argument("--username", default="student02", help="Demo username.")
    parser.add_argument("--password", default="campus123", help="Demo password.")
    parser.add_argument(
        "--screenshots-dir",
        default="../../frontend/src/assets/test-assets/screenshots",
        help="Directory for dashboard screenshots, relative to this script.",
    )
    parser.add_argument(
        "--summary",
        default="../reports/selenium-latest.json",
        help="JSON summary path, relative to this script.",
    )
    parser.add_argument("--headed", action="store_true", help="Run Chrome with a visible window.")
    args = parser.parse_args()

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    script_dir = Path(__file__).resolve().parent
    screenshots_dir = (script_dir / args.screenshots_dir).resolve()
    summary_path = (script_dir / args.summary).resolve()
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    options = Options()
    if not args.headed:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1100")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    chrome_path = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
    if chrome_path.exists():
        options.binary_location = str(chrome_path)

    steps: list[dict] = []
    started_at = now_iso()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    def record(name: str, status: str, detail: str, screenshot_name: str | None = None) -> None:
        item = {"name": name, "status": status, "detail": detail, "at": now_iso()}
        if screenshot_name:
            screenshot_path = screenshots_dir / screenshot_name
            driver.save_screenshot(str(screenshot_path))
            item["screenshotPath"] = f"src/assets/test-assets/screenshots/{screenshot_name}"
        steps.append(item)

    def click_first_enabled(testid: str, label: str) -> None:
        selector = f"[data-testid='{testid}']"

        def enabled_candidate(current_driver):
            for element in current_driver.find_elements(By.CSS_SELECTOR, selector):
                if element.is_displayed() and element.is_enabled():
                    return element
            return False

        element = wait.until(enabled_candidate, message=f"No enabled UI action found for {label}")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        driver.execute_script("arguments[0].click();", element)

    try:
        driver.get(args.base_url)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(., '活动 / BookNest / 审核')]]")
            )
        ).click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']"))).clear()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']").send_keys(args.username)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").clear()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").send_keys(args.password)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "登录成功"))
        record("login", "passed", f"{args.username} 登录成功", "selenium-login.png")

        click_first_enabled("register-activity", "activity registration")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "活动报名成功"))
        record("activity", "passed", "开放活动报名成功", "selenium-activity.png")

        click_first_enabled("reserve-room", "room reservation")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "场地预约申请已提交"))
        record("room", "passed", "可用场地预约申请提交成功", "selenium-room.png")

        click_first_enabled("borrow-device", "device borrow")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "设备借用申请已提交"))
        record("device", "passed", "可用设备借用申请提交成功", "selenium-device.png")

        click_first_enabled("borrow-book", "book borrow")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "图书借阅成功"))
        record("booknest", "passed", "可借图书借阅成功", "selenium-booknest.png")

        click_first_enabled("read-notification", "notification read")
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "通知已标记为已读"))
        record("notification", "passed", "本人通知标记已读成功", "selenium-notification.png")

        summary = {
            "status": "passed",
            "runId": "ui-selenium-latest",
            "browser": "Chrome",
            "startedAt": started_at,
            "finishedAt": now_iso(),
            "baseUrl": args.base_url,
            "steps": steps,
        }
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0
    except Exception as exc:
        failure_path = screenshots_dir / "selenium-failure.png"
        driver.save_screenshot(str(failure_path))
        summary = {
            "status": "failed",
            "runId": "ui-selenium-latest",
            "browser": "Chrome",
            "startedAt": started_at,
            "finishedAt": now_iso(),
            "baseUrl": args.base_url,
            "error": str(exc),
            "failureScreenshot": "src/assets/test-assets/screenshots/selenium-failure.png",
            "steps": steps,
        }
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
