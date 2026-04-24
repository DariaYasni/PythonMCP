from playwright.sync_api import expect
import pytest

def test_open_first_book(page, home_page):
    home_page.open()
    # Метод сам найдет заголовок и кликнет
    expected_title = home_page.open_first_book()
    # Проверяем финальный заголовок страницы
    expect(home_page.header_locator).to_contain_text(expected_title, timeout=10000)