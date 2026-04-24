import pytest
from playwright.sync_api import Page, expect

def test_search_flow_debug(page: Page):
    # 1. Заходим на сайт
    page.goto("https://mwtestconsultancy.co.uk", wait_until="networkidle")
    
    # 2. Открываем поиск
    page.locator("button.gh-search:visible").first.click()
    
    # 3. Ждем фрейм и инпут
    search_portal = page.frame_locator('iframe[title="portal-popup"]')
    search_input = search_portal.locator("input").first
    search_input.wait_for(state="visible", timeout=15000)
    
    # 4. Вводим текст и жмем Enter
    search_input.click()
    search_input.press_sequentially("BDD", delay=150)
    page.keyboard.press("Enter") 
    
    # --- ИЗМЕНЕНИЕ ТУТ ---
    # 5. Вместо поиска списка во фрейме, ждем перехода на новую страницу
    # Мы ищем в URL слово 'bdd'
    page.wait_for_url("**/bdd/**", timeout=15000)
    
    # 6. Проверяем заголовок на уже НОВОЙ странице
    page.wait_for_load_state("networkidle")
    expect(page.locator("h1")).to_contain_text("BDD", ignore_case=True, timeout=15000)

    print("Тест успешно прошел через редирект!")