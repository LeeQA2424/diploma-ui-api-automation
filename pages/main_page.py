import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    URL = "https://www.chitai-gorod.ru/"

    SEARCH_INPUT = (By.NAME, "phrase")

    # стабильный локатор карточек товаров
    SEARCH_RESULTS = (By.CSS_SELECTOR, "a[href*='/product/']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(self.URL)

        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
                ) == "complete"
        )

        self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))

    def get_search_field(self):
        return self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))

    def enter_search_query(self, query: str):
        field = self.get_search_field()

        # очистка поля
        field.click()
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.BACKSPACE)

        field.send_keys(query)

        # иногда первый Enter не срабатывает
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        field.send_keys(Keys.ENTER)

        # ждем загрузку результатов (если они есть)
        try:
            self.wait.until(
                lambda d: len(d.find_elements(*self.SEARCH_RESULTS)) > 0
            )
        except Exception:
            pass

        time.sleep(2)  # даём странице догрузиться

    def get_search_results_count(self):
        return len(self.driver.find_elements(*self.SEARCH_RESULTS))

    def click_first_search_result(self):
        results = self.driver.find_elements(*self.SEARCH_RESULTS)

        if not results:
            raise AssertionError("Нет результатов поиска")

        first = results[0]
        old_url = self.driver.current_url

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", first
        )

        time.sleep(1)

        try:
            first.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", first)

        # ждем переход на другую страницу
        self.wait.until(lambda d: d.current_url != old_url)

    def get_page_title(self):
        return self.driver.title
