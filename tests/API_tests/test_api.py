import pytest
import time
import logging

logger = logging.getLogger(__name__)

# 1. Проверка статус-кода
def test_main_page_status(api):
    response = api.get("/") 
    assert response.status == 200

# 2. Проверка заголовков
def test_main_page_headers(api):
    response = api.get("/") # ИСПРАВЛЕНО: было get_main_page()
    headers = response.headers
    print(f"\nHeaders: {headers}") 
    assert "text/html" in headers.get("content-type", "").lower()
    assert "date" in headers
    assert "cache-control" in headers

# 3. Проверка производительности (Performance)
def test_main_page_performance(api):
    start_time = time.time()
    response = api.get("/") # ИСПРАВЛЕНО: было get_main_page()
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    logger.info(f"API Response time: {duration_ms:.2f}ms")
    assert response.ok
    assert duration_ms < 1500, f"API слишком медленное: {duration_ms:.2f}ms"

# 4. Проверка целостности контента (Content Integrity)
def test_main_page_content_integrity(api):
    response = api.get("/") # ИСПРАВЛЕНО: было get_main_page()
    body = response.text()
    assert "<title>" in body.lower()
    assert len(body) > 100, "Тело ответа слишком короткое"

# 5. Динамическая синхронизация API и UI
def test_latest_article_consistency(api, home_page):
    """Проверяет, что заголовок из UI присутствует в коде API"""
    response = api.get("/") # ИСПРАВЛЕНО: было get_main_page()
    html_content = response.text()

    home_page.open()
    ui_titles = home_page.get_all_article_titles()
    
    assert len(ui_titles) > 0, "Статьи не найдены на странице"
    latest_ui_title = ui_titles[0] 
    
    assert latest_ui_title in html_content
    print(f"\n[OK] Актуальная статья найдена: {latest_ui_title}")

# 6. Параметризованный тест разделов (DDT)
@pytest.mark.parametrize("path, expected_title", [
    ("books", "Books"),        
    ("tools", "Tools"),        
    ("tag/tools", "Tools")     
])
def test_sections_availability(api, path, expected_title):
    """Проверяет доступность подразделов сайта"""
    response = api.get(path)
    print(f"\nChecking URL: {response.url}") 
    assert response.status == 200, f"Раздел {path} недоступен! Статус: {response.status}"
    assert expected_title in response.text(), f"Заголовок '{expected_title}' не найден в ответе"