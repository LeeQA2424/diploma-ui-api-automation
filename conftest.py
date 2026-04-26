import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    # 1. Настройка опций браузера
    options = Options()

    # Отключаем режим автоматизации, который видит сайт
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Добавляем реалистичный User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

    # Запуск в развернутом виде
    options.add_argument("--start-maximized")

    # Рекомендуется добавить для стабильности на Windows
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Скрываем артефакты автоматизации
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 2. Инициализация драйвера
    driver = webdriver.Chrome(options=options)

    # Дополнительно убираем флаг webdriver из navigator
    driver.execute_script(
        "Object.defineProperty(navigator, "
        "'webdriver', {get: () => undefined})"
        )

    yield driver

    # 3. Закрытие браузера
    driver.quit()
