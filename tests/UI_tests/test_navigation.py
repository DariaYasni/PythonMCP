import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

def test_homepage_visual_layout(page: Page):
    home = HomePage(page)
    home.open()
    
    # Проверяем видимость карточек
    expect(home.article_card.first).to_be_visible()
    
    # Проверяем заголовки
    titles = home.get_all_article_titles()
    assert len(titles) > 0, "Заголовки статей не найдены"

def test_navigation_menu_responsive(page: Page):
    home = HomePage(page)
    home.open()
    
    # Переходим в раздел Books
    home.navigate_to_books()
    
    # ИСПРАВЛЕНО: Используем регулярное выражение вместо лямбды
    expect(page).to_have_url(re.compile(r".*/books/.*"))