import re
from pages.home_page import HomePage
from playwright.sync_api import Page, expect

def test_newsletter_subscription_page_load(page: Page):
    home = HomePage(page)
    home.open()
    
    # 1. Проверяем наличие ключевого слова на странице (Consultancy)
    # Это сработает, даже если название сайта — картинка
    expect(page.locator("body")).to_contain_text(re.compile("Consultancy", re.I), timeout=10000)
    
    # 2. Проверяем, что кнопка подписки видна (Newsletter/Subscribe)
    subscribe_btn = page.get_by_text(re.compile(r"Subscribe|Newsletter", re.I)).first
    expect(subscribe_btn).to_be_visible(timeout=10000)
    
    print("\n✓ Тест подписки: Базовая разметка страницы проверена")




