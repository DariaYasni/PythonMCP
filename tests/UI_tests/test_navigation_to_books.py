import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

def test_navigation_to_books(page: Page):
    home = HomePage(page)
    
    # 1. Открываем главную страницу
    # Используем метод из вашего класса HomePage для единообразия
    home.open() 
    page.wait_for_load_state("networkidle")

    # 2. Кликаем по пункту меню "Books"
    # Мы видели на скриншоте, что эта ссылка точно есть в хедере
    books_link = page.get_by_role("link", name="Books", exact=False)
    
    # Кликаем по первой найденной ссылке (обычно в главном меню)
    books_link.first.click()

    # 3. ПРОВЕРКИ
    # А) Ждем, когда URL поменяется на /books/
    expect(page).to_have_url(re.compile(r".*/books/.*", re.I), timeout=15000)
    
    # Б) Проверяем наличие заголовка H1 с текстом Books
    # Это надежнее, чем просто get_by_text, так как мы проверяем структуру страницы
    header = page.locator("h1")
    expect(header).to_contain_text("Books", ignore_case=True, timeout=10000)
    
    print(f"\n✓ Успешный переход в раздел Books. Текущий URL: {page.url}")