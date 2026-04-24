import pytest
from playwright.sync_api import expect

def test_search_valid_book(home_page):
    """Позитивный тест: должен пройти со словом AI"""
    home_page.open()
    
    search_query = "AI" 
    home_page.search_for(search_query)
    
    # Получаем заголовки
    titles = home_page.get_all_article_titles()
    
    # ПРОВЕРКА: Результаты найдены
    assert len(titles) > 0, f"По запросу '{search_query}' ничего не найдено"
    print(f"\nНайдено статей: {len(titles)}")

def test_search_negative_no_results(home_page):
    """Негативный тест: проверка отсутствия результатов"""
    home_page.open()
    
    # Вводим абракадабру
    home_page.search_for("zxcvbnm12345")
    
    # Даем фрейму 2 секунды на обновление (на Ghost Portal это важно)
    home_page.page.wait_for_timeout(2000)
    
    # ПРОВЕРКА: Количество статей в результатах поиска должно быть 0
    is_empty = home_page.is_search_results_empty()
    assert is_empty, "Ожидалось, что результатов не будет, но что-то нашлось!"