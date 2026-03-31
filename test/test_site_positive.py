import allure
from pages.homepage import HomePage


@allure.epic("UI Тестирование")
@allure.feature("Форма регистрации")
@allure.story("Позитивные сценарии")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Успешная отправка формы со всеми полями")
def test_positive(driver):
    with allure.step("Открыть страницу и заполнить форму"):
        homepage = HomePage(driver)
        homepage.open()
        homepage.fill_all_fields("Tata", "Tata57331", "name@example.com")
        homepage.input_message()
    with allure.step("Отправить форму и проверить результат"):
        homepage.submit_and_verify_alert('Message received!')
