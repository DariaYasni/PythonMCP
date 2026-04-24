import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage

def test_search_via_iframe(page):
    # 1. Вместо открытия главной и кликов, идем СРАЗУ на страницу поиска
    # Это работает на Ghost в обход всех фреймов и попапов
    page.goto("https://mwtestconsultancy.co.uk", wait_until="networkidle")
    
    # 2. Находим инпут. После прямого перехода он будет прямо в DOM страницы
    # Пробуем несколько вариантов локаторов для надежности
    search_input = page.locator("input[placeholder*='Search'], input[type='search'], input").first
    
    # Ждем появления и вводим текст
    search_input.wait_for(state="visible", timeout=15000)
    search_input.fill("Playwright")
    
    # 3. Ждем появления результатов (заголовки h3)
    # Используем expect, так как он сам умеет ждать
    first_result = page.locator("h3").first
    expect(first_result).to_be_visible(timeout=15000)
    
    # Выводим результат
    print(f"\n✓ ПОБЕДА! Найден результат: {first_result.text_content()}")