import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="CampusHub login, activity registration, and book borrow smoke test.")
    parser.add_argument("--base-url", default="http://localhost:5173", help="CampusHub frontend URL.")
    parser.add_argument("--username", default="student01", help="Demo username.")
    parser.add_argument("--password", default="campus123", help="Demo password.")
    args = parser.parse_args()

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    options = Options()
    chrome_path = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
    if chrome_path.exists():
        options.binary_location = str(chrome_path)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 12)
    try:
        driver.get(args.base_url)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']"))).clear()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-username']").send_keys(args.username)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").clear()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']").send_keys(args.password)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "登录成功"))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='register-activity']:not(:disabled)"))).click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "活动报名成功"))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='borrow-book']:not(:disabled)"))).click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='success-message']"), "图书借阅成功"))
        return 0
    except Exception:
        driver.save_screenshot(str(Path("selenium-failure.png").resolve()))
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
