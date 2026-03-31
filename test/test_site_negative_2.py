import allure
from pages.homepage import HomePage


@allure.feature("Форма регистрации")
@allure.story("Негативный сценарий")
@allure.title("Отправка формы только с именем")
def test_negative_2(driver):
    homepage = HomePage(driver)
    homepage.open()
    homepage.input_name('Tata')
    homepage.submit_and_expect_no_alert()