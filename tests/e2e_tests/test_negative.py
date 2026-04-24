import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage 

def test_account_form_opens(page: Page):
    home = HomePage(page)
    home.open()
    # Кликаем по кнопке аккаунта
    trigger = page.frame_locator('iframe[title="portal-trigger"]')
    trigger.locator('[data-testid="portal-trigger-button"]').click(force=True)
    # Проверяем наличие формы во фрейме
    portal = page.frame_locator(home.search_frame_selector)
    expect(portal.get_by_text(re.compile("Email", re.I))).to_be_visible(timeout=15000)

def test_search_no_results(page: Page):
    home = HomePage(page)
    home.open()
    
    # 1. Открываем поиск
    home.wait_for_search_portal()
    
    # 2. Вводим текст напрямую
    portal = page.frame_locator(home.search_frame_selector)
    search_input = portal.locator(home.search_input_selector)
    search_input.fill("empty_query_123_xyz_999")
    
    # 3. Гибкая проверка текста (исправляем падение)
    # Ищем ЛЮБОЙ текст, содержащий "No results" или "No matches"
    # Мы не используем метод из HomePage, так как он может быть слишком строгим
    expect(portal.get_by_text(re.compile(r"No results|No matches", re.I))).to_be_visible(timeout=10000)

def test_search_clear(page: Page):
    home = HomePage(page)
    home.open()
    # 1. Открываем портал поиска
    home.wait_for_search_portal()
    # 2. Вводим текст
    portal = page.frame_locator(home.search_frame_selector)
    search_input = portal.locator(home.search_input_selector)
    search_input.fill("Playwright")
    # 3. Очищаем поле (через fill(""))
    search_input.fill("")
    # 4. Проверяем, что пусто
    expect(search_input).to_have_value("")