import re
from pages.home_page import HomePage
from playwright.sync_api import Page, expect

def test_navigate_to_tools(page: Page):
    # 1. Инициализация
    homepage = HomePage(page)
    
    # 2. Открытие страницы с ожиданием полной загрузки сети
    homepage.open()
    page.wait_for_load_state("networkidle") # Ждем, пока запросы затихнут
    
    # 3. Переход в раздел Tools
    # Если метод кликает по ссылке, Playwright сам подождет появления элемента
    homepage.navigate_to("Tools")
    
    # --- БЛОК СТАБИЛЬНЫХ ПРОВЕРОК (Используют умные ожидания) ---
    
    # А) Проверка URL (самая быстрая и надежная проверка перехода)
    # Используем re.I для игнорирования регистра (Tools vs tools)
    expect(page).to_have_url(re.compile(r".*/tools/.*", re.I), timeout=15000)
    
    # Б) Проверка Title вкладки
    expect(page).to_have_title(re.compile("Tools", re.I), timeout=15000)
    
    # В) Проверка визуального заголовка (H1 или Header)
    # Вместо assert homepage.check_page_header, который возвращает bool,
    # используем локатор напрямую через expect. 
    # Так Playwright будет ждать появления текста до 15 секунд.
    header_locator = page.locator("h1") # Замените на ваш селектор заголовка, если он другой
    expect(header_locator).to_contain_text("Tools", ignore_case=True, timeout=15000)