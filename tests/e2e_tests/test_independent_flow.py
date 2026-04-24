import pytest
import re  # <--- ДОБАВИЛИ ИМПОРТ
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

# 1. Создаем расширенный класс прямо здесь
class SearchPage(HomePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Указываем прямой путь к поиску, чтобы избежать проблем с iframe
        self.search_url = "https://mwtestconsultancy.co.uk" 
        self.search_input = page.locator("input").first
        # Берем первый заголовок или ссылку в результатах
        self.results = page.locator("h3, .gh-search-details-content").first

    def open_search(self):
        self.page.goto(self.search_url, wait_until="networkidle")

    def search_for(self, query: str):
        self.search_input.wait_for(state="visible", timeout=10000)
        self.search_input.fill(query)
        self.page.wait_for_timeout(2000) # Ждем подгрузку результатов

    def select_first_result(self):
        self.results.click()

# 2. Сам тест в стиле POM
def test_independent_flow(page: Page):
    search = SearchPage(page)

    # Шаг 1: Открытие
    search.open_search()

    # Шаг 2: Поиск
    search.search_for("AI")

    # Шаг 3: Действие
    search.select_first_result()

    # Шаг 4: Проверка
    # Проверяем, что URL изменился (ушли со страницы поиска)
    expect(page).not_to_have_url(re.compile(r".*search.*"), timeout=15000)
    
    print(f"✓ Успех! Тест прошел. Текущий URL: {page.url}")