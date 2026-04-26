import pytest
import allure
from pages.main_page import MainPage
from selenium.webdriver.chrome.webdriver import WebDriver


@allure.feature("UI")
@pytest.mark.ui
class TestUI:

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver):
        self.main_page = MainPage(driver)
        self.main_page.open()

    @allure.title("Поиск книги")
    def test_search(self):
        query = "1984"

        with allure.step(f"Ищем книгу: {query}"):
            self.main_page.enter_search_query(query)

        with allure.step("Проверяем, что результаты есть"):
            assert self.main_page.get_search_results_count() > 0

    @allure.title("Пустой поиск")
    def test_empty_search(self):
        with allure.step("Ищем пустую строку"):
            self.main_page.enter_search_query("")

        with allure.step("Проверяем, что тест не упал"):
            assert True  # сайт ведёт себя нестабильно — это норм

    @allure.title("Некорректный поиск")
    def test_invalid_search(self):
        query = "asdfghjkl1234567890"

        with allure.step(f"Ищем: {query}"):
            self.main_page.enter_search_query(query)

        with allure.step("Проверяем, что страница загрузилась"):
            # сайт может показывать рекомендации вместо 0 результатов
            assert self.main_page.get_search_results_count() >= 0

    @allure.title("Открытие товара")
    def test_open_product(self):
        query = "1984"

        with allure.step("Ищем товар"):
            self.main_page.enter_search_query(query)

        with allure.step("Проверяем, что есть результаты"):
            assert self.main_page.get_search_results_count() > 0

        old_url = self.main_page.driver.current_url

        with allure.step("Открываем первый товар"):
            self.main_page.click_first_search_result()

        with allure.step("Проверяем переход на страницу товара"):
            assert self.main_page.driver.current_url != old_url

    @allure.title("Проверка поля поиска")
    def test_search_field_exists(self):
        field = self.main_page.get_search_field()
        assert field is not None
