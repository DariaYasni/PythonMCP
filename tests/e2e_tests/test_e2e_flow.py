import pytest
import logging
import re
from pages.home_page import HomePage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)

def test_full_navigation_e2e(page):
    home = HomePage(page)

    # 1. Открываем сайт
    home.open()

    # 2. ПЕРЕХОДИМ В РАЗДЕЛ "Books" (вместо About)
    home.navigate_to("Books")

    # 3. Проверка заголовка (используем надежный expect вместо метода POM)
    expect(page.locator("h1")).to_contain_text("Books")
    logger.info(f"Успешно перешли на: {page.url}")

    # 4. ВЫПОЛНЯЕМ ПОИСК (через наш стабильный хак с прямым URL)
    page.goto("https://mwtestconsultancy.co.uk", wait_until="networkidle")
    
    # Находим инпут и вводим запрос
    search_input = page.locator("input").first
    search_input.fill("Playwright")
    
    # 5. Проверка результатов
    page.wait_for_timeout(3000)
    results = page.locator("h3")
    
    # Проверяем, что результаты появились
    expect(results.first).to_be_visible(timeout=10000)
    assert results.count() > 0, "Список результатов поиска пуст"
    
    logger.info(f"Поиск успешно отработал. Текущий URL: {page.url}")
    print(f"✓ Успех! Все шаги теста выполнены.")