from playwright.sync_api import Page, expect

def test_search_logic(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # 1. Переход на сайт
    page.goto("https://mwtestconsultancy.co.uk", wait_until="networkidle", timeout=30000)

    # 2. Клик по кнопке (уже исправленный селектор)
    search_button = page.locator("button[data-ghost-search]:visible")
    search_button.click()

    # 3. Работа с iframe
    # Сначала дождемся, что сам iframe прикрепился к странице
    portal_locator = page.locator('iframe[title="portal-popup"]')
    portal_locator.wait_for(state="attached", timeout=15000)
    
    # Создаем локатор фрейма
    portal = page.frame_locator('iframe[title="portal-popup"]')
    
    # Ищем инпут. В Ghost Search он часто имеет атрибут placeholder="Search posts..."
    # Попробуем использовать более универсальный селектор для инпута
    search_input = portal.locator('input[placeholder*="Search"], input[type="search"]').first
    
    # 4. Ввод текста
    # Используем click() перед fill(), чтобы активировать поле внутри фрейма
    search_input.wait_for(state="visible", timeout=15000)
    search_input.click()
    search_input.fill("Testing")
    
    # 5. Проверка
    expect(search_input).to_have_value("Testing")


