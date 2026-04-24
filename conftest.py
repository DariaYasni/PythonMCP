import os
import pytest
import allure
from playwright.sync_api import Playwright

# 1. Фикстура для создания Environment в Allure (Сессионная)
@pytest.fixture(scope="session", autouse=True)
def create_allure_environment():
    """
    Автоматически создает файл environment.properties в папке allure-results.
    """
    yield  # Ждем завершения всех тестов
    
    allure_results_path = "allure-results"
    
    if not os.path.exists(allure_results_path):
        os.makedirs(allure_results_path)
    
    env_file_path = os.path.join(allure_results_path, "environment.properties")
    with open(env_file_path, "w") as f:
        f.write("Project=MyProject\n")
        f.write("Browser=Chromium\n")
        f.write("URL=https://mwtestconsultancy.co.uk\n")

# 2. Фикстура для API
@pytest.fixture
def api(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url="https://mwtestconsultancy.co.uk"
    )
    yield request_context
    request_context.dispose()

# 3. Фикстура для Home Page
@pytest.fixture
def home_page(page):
    from pages.home_page import HomePage 
    return HomePage(page)

# 4. Хук для скриншотов при падении
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = None
        if "home_page" in item.funcargs:
            page = item.funcargs["home_page"].page
        elif "page" in item.funcargs:
            page = item.funcargs["page"]

        if page:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"Failure_Screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")