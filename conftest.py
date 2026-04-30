import os
import pytest
import allure
import json
from playwright.sync_api import Playwright

# 1. Улучшенная фикстура для окружения И добавление категорий
@pytest.fixture(scope="session", autouse=True)
def setup_allure_assets():
    yield  # Ждем окончания тестов
    
    results_dir = "allure-results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Создаем environment.properties (как у вас было)
    with open(f"{results_dir}/environment.properties", "w") as f:
        f.write("Project=MyProject\nBrowser=Chromium\nURL=https://mwtestconsultancy.co.uk\n")
    
    # --- НОВОЕ: Добавляем категории ошибок ---
    categories = [
        {
            "name": "Skipped tests",
            "matchedStatuses": ["skipped"]
        },
        {
            "name": "Infrastructure issues (Timeouts)",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*timeout.*"
        },
        {
            "name": "Product defects (Assertion errors)",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*"
        },
        {
            "name": "Test data issues",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*not found.*"
        }
    ]
    with open(f"{results_dir}/categories.json", "w") as f:
        json.dump(categories, f, indent=4)

# 2. Фикстуры для API и Page Object (оставляем ваши)
@pytest.fixture
def api(playwright: Playwright):
    request_context = playwright.request.new_context(base_url="https://mwtestconsultancy.co.uk")
    yield request_context
    request_context.dispose()

@pytest.fixture
def home_page(page):
    from pages.home_page import HomePage 
    return HomePage(page)

# 3. Продвинутый хук для отладки при падении
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Ищем страницу среди аргументов теста
        page = item.funcargs.get("page") or (item.funcargs.get("home_page").page if "home_page" in item.funcargs else None)

        if page:
            # 📸 Скриншот
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            # 📄 Исходный код страницы (помогает понять, почему не найден элемент)
            allure.attach(
                page.content(),
                name=f"HTML_Source_{item.name}",
                attachment_type=allure.attachment_type.HTML
            )
          