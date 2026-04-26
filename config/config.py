from selenium.webdriver.common.by import By

# UI
BASE_URL = "https://www.chitai-gorod.ru"
SEARCH_QUERY = "1984"

# Browser
HEADLESS_MODE = False
TIMEOUT = 10

# API
API_URL = "https://api.chitai-gorod.ru"

# Locators
LOCATORS = {
    "search_field": (By.CSS_SELECTOR, "input[type='search']"),
    "search_button": (By.CSS_SELECTOR, "button[type='submit']"),
    "results_container": (By.CSS_SELECTOR, ".products-list"),
    "product_card": (By.CSS_SELECTOR, ".product-card"),
    "first_product": (By.CSS_SELECTOR, ".product-card"),
    "error_message": (By.XPATH, "//*[contains(text(),'Ничего не найдено')]"),
}
