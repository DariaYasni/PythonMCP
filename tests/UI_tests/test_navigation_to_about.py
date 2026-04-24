import re
import pytest
from pages.home_page import HomePage
from playwright.sync_api import Page, expect

def test_navigation_to_any_menu_item(page: Page):
    home = HomePage(page)
    
    # 1. Настройка окружения
    # Устанавливаем десктопный размер, чтобы видеть полное меню
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    # 2. Открытие страницы
    home.open()
    
    # Сохраняем текущий URL для сравнения
    old_url = page.url
    print(f"\nНачальный URL: {old_url}")

    # 3. Поиск ссылок в меню
    # На сайте Ghost (mwtestconsultancy) меню обычно находится в .gh-head-menu или просто в nav
    menu_links = page.locator(".gh-head-menu a, nav a, ul.nav li a").filter(has_text=re.compile(r"\w+"))
    
    # Ждем появления хотя бы одной ссылки
    menu_links.first.wait_for(state="visible", timeout=10000)
    
    count = menu_links.count()
    assert count > 0, "Меню навигации не найдено на странице"
    print(f"Найдено пунктов меню: {count}")

    # 4. Взаимодействие с первым пунктом
    # Игнорируем ссылку Home (так как она не изменит URL), берем вторую если первая - Home
    target_link = menu_links.nth(1) if "home" in menu_links.first.inner_text().lower() else menu_links.first
    
    link_text = target_link.inner_text().strip()
    print(f"Кликаем по пункту меню: {link_text}")
    
    # 5. Клик и ожидание перехода
    target_link.click(force=True)
    
    # Ждем, пока URL изменится (не будет равен начальному)
    # expect будет перепроверять это условие в течение 10 секунд
    expect(page).not_to_have_url(old_url, timeout=10000)

    # 6. Финальные проверки
    new_url = page.url
    print(f"✓ Успешный переход! Новый URL: {new_url}")
    
    # Проверка на 404
    expect(page).not_to_have_title(re.compile("404|Not Found", re.I))
    
    # Делаем скриншот результата
    page.screenshot(path="tests/UI_tests/screenshots/navigation_test_success.png")

    assert new_url != old_url, f"URL должен был измениться после клика по {link_text}"