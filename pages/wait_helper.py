import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from typing import List, Tuple, Any
import time


class WaitHelper:
    def __init__(self, driver: WebDriver, default_timeout: int = 10, poll_frequency: float = 0.5):
        self.driver = driver
        self.default_timeout = default_timeout
        self.poll_frequency = poll_frequency

    def _get_wait(self, timeout: int = None) -> WebDriverWait:
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout, self.poll_frequency)

    @allure.step("Ожидание видимости элемента")
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="element_not_visible",
                          attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Ожидание кликабельности элемента")
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="element_not_clickable",
                          attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Поиск элементов с повторными попытками")
    def find_elements_with_retry(self, locator: Tuple[str, str], retries: int = 3, timeout: int = 2) -> List[
        WebElement]:
        for attempt in range(retries):
            elements = self.driver.find_elements(*locator)
            if elements:
                allure.attach(f"Найдено {len(elements)} элементов с {attempt + 1} попытки",
                              name="elements_found",
                              attachment_type=allure.attachment_type.TEXT)
                return elements
            if attempt < retries - 1:
                time.sleep(timeout)
        allure.attach(self.driver.get_screenshot_as_png(), name="elements_not_found",
                      attachment_type=allure.attachment_type.PNG)
        return []

    @allure.step("Ожидание появления alert")
    def wait_for_alert(self, timeout: int = None) -> Any:
        wait = self._get_wait(timeout)
        try:
            return wait.until(EC.alert_is_present())
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="alert_not_present",
                          attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout: int = None):
        wait = self._get_wait(timeout)
        try:
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="page_load_timeout",
                          attachment_type=allure.attachment_type.PNG)
            raise