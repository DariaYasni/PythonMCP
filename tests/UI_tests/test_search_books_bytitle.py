import pytest
from pages.home_page import HomePage

def test_search_for_books(page):
    home = HomePage(page)
    home.open()
    
    # 1. Берем слово для поиска (из первой статьи)
    page.wait_for_selector("article h2, .gh-card-title", timeout=10000)
    full_title = page.locator("article h2, .gh-card-title").first.inner_text()
    search_term = full_title.replace(',', '').replace('.', '').split()[0]
    print(f"\n[DEBUG] Ищем слово: {search_term}")

    # 2. Открываем поиск (Control+K)
    page.keyboard.press("Control+K")
    page.wait_for_timeout(2000)

    # 3. Печатаем по буквам и ЖМЕМ ENTER (это критично для Ghost)
    page.keyboard.type(search_term, delay=200)
    page.keyboard.press("Enter") 
    page.wait_for_timeout(3000) # Даем время на загрузку результатов

    # 4. Ищем результаты ВО ВСЕХ ФРЕЙМАХ
    titles = []
    for _ in range(5): # 5 попыток
        for frame in page.frames:
            try:
                # Ищем любой текст внутри фрейма, который содержит наше слово
                # Селектор :has-text — самый мощный способ найти результат
                found = frame.locator(f"div:has-text('{search_term}'), h2, a").all_inner_texts()
                valid_titles = [t.lower().strip() for t in found if len(t.strip()) > 5]
                if any(search_term.lower() in t for t in valid_titles):
                    titles = valid_titles
                    break
            except:
                continue
        if titles: break
        page.wait_for_timeout(1500)

    print(f"[DEBUG] Найдено результатов: {len(titles)}")
    print(f"[DEBUG] Список: {titles[:3]}...") # Выводим первые три
    
    assert len(titles) > 0, f"Поиск по слову '{search_term}' не выдал результатов."
    assert any(search_term.lower() in t for t in titles), f"Слово '{search_term}' не найдено в выдаче."