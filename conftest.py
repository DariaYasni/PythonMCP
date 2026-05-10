import os
import json
import pytest
import allure
from playwright.sync_api import Playwright

# --- 1. SETTINGS & CONSTANTS ---


@pytest.fixture
def api_url():
    """Возвращает базовый URL как строку (нужно для ваших текущих тестов)"""
    return "https://restful-booker.herokuapp.com"


# --- 2. ALLURE: Настройка окружения и категорий ---


@pytest.fixture(scope="session", autouse=True)
def setup_allure_assets():
    yield
    results_dir = "allure-results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    with open(f"{results_dir}/environment.properties", "w") as f:
        f.write(
            "Project=MW_Test_Consultancy\n"
            "UI_URL=https://mwtestconsultancy.co.uk\n"
            "API_URL=https://restful-booker.herokuapp.com\n"
            "Browser=Chromium\n"
        )

    categories = [
        {"name": "Skipped tests", "matchedStatuses": ["skipped"]},
        {
            "name": "Infrastructure issues (Timeouts)",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*timeout.*",
        },
        {
            "name": "Product defects (Assertion errors)",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*",
        },
        {
            "name": "Test data issues",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*not found.*",
        },
    ]
    with open(f"{results_dir}/categories.json", "w") as f:
        json.dump(categories, f, indent=4)


# --- 3. API FIXTURES ---


@pytest.fixture
def api(playwright: Playwright):
    """Контекст для работы с основным сайтом Марка"""
    request_context = playwright.request.new_context(
        base_url="https://mwtestconsultancy.co.uk"
    )
    yield request_context
    request_context.dispose()


@pytest.fixture
def booker_api(playwright: Playwright, api_url):
    """Контекст Playwright, использующий уже определенный api_url"""
    request_context = playwright.request.new_context(base_url=api_url)
    yield request_context
    request_context.dispose()


# --- 4. UI & PAGE OBJECTS ---


@pytest.fixture
def home_page(page):
    from pages.home_page import HomePage

    return HomePage(page)


# --- 5. ХУК ДЛЯ СКРИНШОТОВ ПРИ ПАДЕНИИ ---


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if not page and "home_page" in item.funcargs:
            page = item.funcargs.get("home_page").page

        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                page.content(),
                name=f"HTML_Source_{item.name}",
                attachment_type=allure.attachment_type.HTML,
            )
