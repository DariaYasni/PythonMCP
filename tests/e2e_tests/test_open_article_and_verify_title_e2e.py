import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage  # Проверьте, что путь к файлу верный

def test_open_article_and_verify_title(page: Page):
    # 1. Инициализируем Page Object
    home = HomePage(page)
    
    # 2. Открываем главную страницу
    # Внутри метода open теперь стоит правильное ожидание domcontentloaded
    home.open()
    
    # 3. Используем метод для открытия статьи
    # Он сам найдет первую карточку, кликнет по a.gh-card-link 
    # и дождется, пока URL перестанет быть "/"
    expected_title = home.open_first_book()
    
    # 4. Проверяем заголовок на открывшейся странице
    # Внутри check_title теперь встроен надежный expect с таймаутом
    home.check_title(expected_title)

    print(f"Тест успешно завершен! Открыта статья: {expected_title}")