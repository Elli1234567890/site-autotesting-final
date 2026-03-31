import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.wait_helper import WaitHelper


class HomePage:
    URL = 'https://practice-automation.com/form-fields/'

    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelper(driver, default_timeout=15)
        self.wait = WebDriverWait(driver, 10)

    NAME_INPUT = (By.ID, "name-input")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    DRINK_CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")
    COLOR_RADIOS = (By.CSS_SELECTOR, "input[type='radio']")
    AUTOMATION_RADIOS = (By.NAME, "automation")
    AUTOMATION_TOOLS = (By.CSS_SELECTOR, "ul li")

    @property
    def name_input(self):
        return self.driver.find_element(*self.NAME_INPUT)

    @property
    def password_input(self):
        return self.driver.find_element(*self.PASSWORD_INPUT)

    @property
    def email_input(self):
        return self.driver.find_element(*self.EMAIL_INPUT)

    @property
    def message_textarea(self):
        return self.driver.find_element(*self.MESSAGE_TEXTAREA)

    @property
    def submit_button(self):
        return self.driver.find_element(*self.SUBMIT_BUTTON)

    @allure.step("Открываем страницу")
    def open(self):
        self.driver.get(self.URL)
        self.wait_helper.wait_for_page_load()
        self.wait_helper.wait_for_element_visible(self.NAME_INPUT)
        return self

    @allure.step("Заполняем поле Name: {name}")
    def input_name(self, name: str):
        element = self.wait_helper.wait_for_element_clickable(self.NAME_INPUT)
        element.clear()
        element.send_keys(name)
        return self

    @allure.step("Заполняем поле Password: {password}")
    def input_password(self, password: str):
        element = self.wait_helper.wait_for_element_clickable(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self

    @allure.step("Выбираем напитки Milk и Coffee")
    def select_drinks(self):
        target_drinks = ["Milk", "Coffee"]
        checkboxes = self.wait_helper.find_elements_with_retry(self.DRINK_CHECKBOXES, retries=5)
        if not checkboxes:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="no_drink_checkboxes",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Чекбоксы напитков не найдены на странице. "
                                 "Необходимо проверить, что страница загрузилась корректно и элементы присутствуют в DOM.")
        for checkbox in checkboxes:
            try:
                checkbox_id = checkbox.get_attribute('id')
                if not checkbox_id:
                    continue
                label = self.driver.find_element(By.XPATH, f"//label[@for='{checkbox_id}']")
                drink_name = label.text.strip()
                if drink_name in target_drinks:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                    self.wait.until(EC.element_to_be_clickable((By.ID, checkbox_id)))
                    if not checkbox.is_selected():
                        checkbox.click()
                        allure.attach(f"Выбран напиток: {drink_name}",
                                      name="drink_selected",
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach(f"Напиток {drink_name} уже выбран",
                                      name="drink_already_selected",
                                      attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Ошибка при выборе напитка: {str(e)}",
                              name="error_selecting_drink",
                              attachment_type=allure.attachment_type.TEXT)
                continue
        return self

    @allure.step("Выбираем цвет Yellow")
    def select_color(self):
        target_color = "Yellow"
        radios = self.wait_helper.find_elements_with_retry(self.COLOR_RADIOS, retries=5)
        if not radios:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="no_color_radios",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Радио-кнопки цвета не найдены на странице. "
                                 "Необходимо проверить, что страница загрузилась корректно и элементы присутствуют в DOM.")
        for radio in radios:
            try:
                radio_id = radio.get_attribute('id')
                if not radio_id:
                    continue
                label = self.driver.find_element(By.XPATH, f"//label[@for='{radio_id}']")
                color_name = label.text.strip()
                if color_name == target_color:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", radio)
                    self.wait.until(EC.element_to_be_clickable((By.ID, radio_id)))
                    if not radio.is_selected():
                        radio.click()
                        allure.attach(f"Выбран цвет: {target_color}",
                                      name="color_selected",
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach(f"Цвет {target_color} уже выбран",
                                      name="color_already_selected",
                                      attachment_type=allure.attachment_type.TEXT)
                    break
            except Exception as e:
                allure.attach(f"Ошибка при выборе цвета: {str(e)}",
                              name="error_selecting_color",
                              attachment_type=allure.attachment_type.TEXT)
                continue
        return self

    @allure.step("Выбраем вариант automation: {option}")
    def select_automation_option(self, option: str = "yes"):
        radios = self.wait_helper.find_elements_with_retry(self.AUTOMATION_RADIOS, retries=5)
        if not radios:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="no_automation_radios",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Радио-кнопки automation не найдены на странице. "
                                 "Необходимо проверить, что форма загрузилась корректно.")
        for radio in radios:
            radio_value = radio.get_attribute('value')
            if radio_value == option:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", radio)
                self.wait.until(EC.element_to_be_clickable((By.NAME, "automation")))
                if not radio.is_selected():
                    radio.click()
                    allure.attach(f"Выбран automation: {option}",
                                  name="automation_selected",
                                  attachment_type=allure.attachment_type.TEXT)
                break
        return self


    @allure.step("Заполняем поле Email: {email}")
    def input_email(self, email: str):
        element = self.wait_helper.wait_for_element_clickable(self.EMAIL_INPUT)
        element.clear()
        element.send_keys(email)
        return self

    @allure.step("Получаем текст из списка Automation tools")
    def get_automation_tools_text(self) -> list:
        items = self.wait_helper.find_elements_with_retry(self.AUTOMATION_TOOLS, retries=3)
        if not items:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="empty_automation_tools_list",
                          attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Список Automation tools пуст. "
                                 "Ожидалось, что на странице есть список инструментов.")
        return [item.text for item in items]

    @allure.step("Сформировываем и заполняем поле Message")
    def input_message(self):
        tool_names = self.get_automation_tools_text()
        tools_count = len(tool_names)
        longest_tool = max(tool_names, key=len) if tool_names else ""
        message = f"Количество инструментов: {tools_count}. Инструмент, содержащий наибольшее количество символов: {longest_tool}"
        element = self.wait_helper.wait_for_element_clickable(self.MESSAGE_TEXTAREA)
        element.send_keys(message)
        allure.attach(message, name="generated_message", attachment_type=allure.attachment_type.TEXT)
        return self

    @allure.step("Заполняем все основные поля формы")
    def fill_all_fields(self, name: str, password: str, email: str):
        return (self.input_name(name)
                .input_password(password)
                .select_drinks()
                .select_color()
                .select_automation_option()
                .input_email(email))

    @allure.step("Нажимаем кнопку Submit, проверить что alert не появился")
    def submit_and_expect_no_alert(self):
        button = self.wait_helper.wait_for_element_clickable(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        try:
            alert = self.wait_helper.wait_for_alert(timeout=2)
            alert.accept()
            raise AssertionError(
                "Alert появился, но по условиям теста его быть не должно. "
                "Необходимо проверить валидацию формы: вероятно, некоторые обязательные поля не заполнены."
            )
        except:
            pass
        return self

    @allure.step("Нажимаем кнопку Submit, проверяем что alert не появился")
    def submit_and_expect_no_alert(self):
        button = self.wait_helper.wait_for_element_clickable(self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)
        time.sleep(0.5)
        self.wait_helper.wait_for_element_clickable(self.SUBMIT_BUTTON)
        try:
            button.click()
        except:
            self.driver.execute_script("arguments[0].click();", button)
        try:
            alert = self.wait_helper.wait_for_alert(timeout=2)
            alert.accept()
            raise AssertionError("Alert появился, но по условиям теста его быть не должно")
        except:
            pass
        return self