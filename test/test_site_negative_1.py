import allure
from pages.homepage import HomePage


@allure.feature("Форма регистрации")
@allure.story("Негативный сценарий")
@allure.title("Отправка формы без имени")
def test_negative_1(driver):
    homepage = HomePage(driver)
    homepage.open()
    homepage.input_password('Tata57331')
    homepage.select_drinks()
    homepage.select_color()
    homepage.select_automation_option()
    homepage.input_email('name@example.com')
    homepage.input_message()
    homepage.submit_and_expect_no_alert()