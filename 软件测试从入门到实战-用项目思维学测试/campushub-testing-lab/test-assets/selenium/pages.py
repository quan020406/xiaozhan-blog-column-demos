from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CampusHubPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, base_url):
        self.driver.get(base_url)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']")))

    def login(self, username, password):
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']")))
        username_input.clear()
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-password']")
        password_input.clear()
        password_input.send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-submit']").click()
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-testid='service-status']"), "后端在线"))

    def go_to_nav(self, label):
        self.driver.find_element(By.XPATH, f"//button[.//span[contains(., '{label}')]]").click()

    def wait_for_action(self, test_id):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-testid='{test_id}']")))

    def click_first_enabled(self, test_id):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, f"[data-testid='{test_id}']")
        button = next((item for item in buttons if item.is_enabled()), None)
        if button is None:
            return False
        button.click()
        return True

    def wait_for_feedback(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='error-message'], [data-testid='success-message']")
            )
        )
