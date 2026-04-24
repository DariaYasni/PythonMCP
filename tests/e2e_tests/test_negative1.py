import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage 

# Список тестовых данных: (текст_запроса, название_кейса)
bad_queries = [
    ("!@#$%^&*", "special_chars"),
    ("1234567890", "digits"),
    ("ОченьДлиннаяСтрокаКоторойНетНаСайте", "long_string"),
    ("    ", "spaces"),
    ("ПриветМир", "cyrillic")
]

@pytest.mark.parametrize("search_query, label", bad_queries)
def test_search_no_results_parametrized(page: Page, search_query, label):
    home = HomePage(page)
    home.open()
    
    # 1. Открываем поиск
    home.wait_for_search_portal()
    
    # 2. Вводим данные из параметров
    portal = page.frame_locator(home.search_frame_selector)
    search_input = portal.locator(home.search_input_selector)
    
    print(f"Запуск кейса: {label} с запросом: {search_query}")
    search_input.fill(search_query)
    
    # 3. Проверка сообщения
    expect(portal.get_by_text(re.compile(r"No results|No matches", re.I))).to_be_visible(timeout=10000)