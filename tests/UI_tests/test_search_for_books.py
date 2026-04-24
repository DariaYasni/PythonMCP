from pages.home_page import HomePage # Импортируем ваш Page Object
from playwright.sync_api import Page, expect

def test_search_for_books_with_pom(page: Page):
    # 1. Инициализируем Page Object
    home_page = HomePage(page)
    
    # 2. Действия через методы класса (вся "грязь" с iframe спрятана внутри)
    home_page.open()
    portal = home_page.wait_for_search_portal() # Метод вернет нам объект фрейма
    
    # 3. Взаимодействие
    search_input = portal.locator("input").first
    search_input.fill("Books")
    
    # 4. Проверка
    expect(search_input).to_have_value("Books")
