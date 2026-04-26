import pytest
import requests
import allure
from config.config import API_URL, SEARCH_QUERY


@pytest.mark.api
class TestAPI:

    @allure.title("Поиск книги через API")
    @allure.story("API Поиск")
    def test_search_books(self):
        with allure.step("Отправляем запрос"):
            response = requests.get(
                f"{API_URL}/search",
                params={"phrase": SEARCH_QUERY},
                headers={"User-Agent": "Mozilla/5.0"}
            )

        with allure.step("Проверяем статус"):
            assert response.status_code == 200

        with allure.step("Проверяем, что ответ не пустой"):
            assert len(response.text) > 0

    @allure.title("Пустой поиск API")
    @allure.story("API Поиск")
    def test_empty_search(self):
        with allure.step("Отправляем пустой запрос"):
            response = requests.get(
                f"{API_URL}/search",
                params={"phrase": ""},
                headers={"User-Agent": "Mozilla/5.0"}
            )

        with allure.step("Проверяем статус"):
            assert response.status_code == 200

    @allure.title("Некорректный поиск API")
    @allure.story("API Поиск")
    def test_invalid_search(self):
        query = "asdfghjkl1234567890"

        with allure.step("Отправляем запрос"):
            response = requests.get(
                f"{API_URL}/search",
                params={"phrase": query},
                headers={"User-Agent": "Mozilla/5.0"}
            )

        with allure.step("Проверяем статус"):
            assert response.status_code == 200

        with allure.step("Проверяем, что ответ есть"):
            assert len(response.text) > 0

    @allure.title("Невалидный endpoint")
    @allure.story("API Ошибки")
    def test_invalid_endpoint(self):
        with allure.step("Отправляем запрос"):
            response = requests.get(f"{API_URL}/invalid")

        with allure.step("Проверяем статус (API защищен)"):
            assert response.status_code in [403, 404]

    @allure.title("Проверка Content-Type")
    @allure.story("API Структура")
    def test_response_structure(self):
        with allure.step("Делаем запрос"):
            response = requests.get(
                f"{API_URL}/search",
                params={"phrase": SEARCH_QUERY}
            )

        with allure.step("Проверяем заголовок"):
            assert "content-type" in response.headers

    @allure.title("Невалидная авторизация")
    @allure.story("API Авторизация")
    def test_invalid_auth(self):
        with allure.step("Отправляем запрос с токеном"):
            response = requests.get(
                f"{API_URL}/search",
                params={"phrase": SEARCH_QUERY},
                headers={"Authorization": "Bearer invalid"}
            )

        with allure.step("Проверяем статус"):
            assert response.status_code in [200, 403]
