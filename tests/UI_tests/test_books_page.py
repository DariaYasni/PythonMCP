import pytest
import re
from pages.home_page import HomePage  
from playwright.sync_api import expect

@pytest.fixture
def home_page(page):
    return HomePage(page)

def test_navigation_to_books(home_page):
    # 1. Открываем сайт
    home_page.open()
    
    # 2. Переходим в раздел Books
    home_page.navigate_to("Books")
    
    # 3. Усиленная проверка: ждем, пока URL изменится на /books/
    # Это гарантирует, что переход завершился
    expect(home_page.page).to_have_url(re.compile(r".*/books/"), timeout=15000)
    
    # 4. Проверяем заголовок (используем ваш метод-алиас)
    # Используем проверку, что текст СОДЕРЖИТ "Books" (регистр не важен)
    home_page.check_title("Books")
    
    # 5. Собираем заголовки
    # Даем небольшую паузу, чтобы карточки книг успели отрисоваться через JS
    home_page.page.wait_for_timeout(2000)
    titles = home_page.get_all_article_titles()
    
    # Печать для отладки
    print(f"\nНайдено книг: {len(titles)}")
    if len(titles) > 0:
        print(f"Первая книга: {titles[0]}")
    
    # 6. Проверяем, что книги найдены
    assert len(titles) > 0, f"Список книг пуст на странице {home_page.page.url}"
