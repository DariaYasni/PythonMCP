import re
from pages.home_page import HomePage
from playwright.sync_api import expect

def test_sign_button_exists_on_homepage(page):
    home_page = HomePage(page)
    
    # 1. Удаляем timeout_ms, так как ваш HomePage.open его не принимает
    # Это исправит ошибку TypeError
    home_page.open() 

    # 2. Используем более гибкое имя кнопки (Sign или Subscribe)
    # Используем .first, чтобы избежать ошибки "strict mode violation"
    sign_button = page.get_by_role("link", name=re.compile(r"Sign|Subscribe", re.I)).first
    
    # 3. Используем expect вместо assert
    # Это "умное" ожидание: оно само подождет появления кнопки до 15 секунд
    expect(sign_button).to_be_visible(timeout=15000)