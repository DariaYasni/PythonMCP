import re
import pytest
from playwright.sync_api import expect

def test_search_opens(page):
    # 1. Открываем сайт
    page.goto("https://mwtestconsultancy.co.uk", wait_until="domcontentloaded")

    # 2. Кликаем по кнопке поиска
    page.get_by_label("Search this site").filter(visible=True).first.click()
    
    # 3. Работаем с конкретным фреймом портала
    # Мы увидели в логе, что поиск находится в iframe с title="portal-popup"
    search_frame = page.frame_locator("iframe[title='portal-popup']")
    
    # 4. Ищем инпут внутри этого фрейма
    # Используем максимально простой локатор "input", так как во фрейме поиска он обычно один
    search_input = search_frame.locator("input").first
    
    # 5. Проверка видимости и ввод текста
    # Увеличим таймаут, так как фрейм с попапом может подгружаться чуть дольше
    expect(search_input).to_be_visible(timeout=15000)
    search_input.fill("Playwright")
    
    # 6. Проверка результата
    expect(search_input).to_have_value("Playwright")