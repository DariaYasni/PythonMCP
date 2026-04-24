import re
from playwright.sync_api import expect
from pages.home_page import HomePage

def test_navigation_books_section_e2e(page): # Переименовали тест
    home = HomePage(page)
    
    # 1. Открываем сайт
    home.open()
    
    # 2. Кликаем по существующему разделу "Books"
    # Метод navigate_to в HomePage сработает, так как текст "Books" есть в DOM
    home.navigate_to("Books") 
    
    # 3. Проверка URL (теперь ищем 'books' вместо 'about')
    expect(page).to_have_url(re.compile(r"books", re.I), timeout=10000)
    
    # 4. Проверка заголовка на странице
    expect(page.locator("h1")).to_contain_text("Books")
    
    print(f"✓ Успех! Страница Books загружена: {page.url}")