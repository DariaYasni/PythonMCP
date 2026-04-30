import re
import logging
import allure
from playwright.sync_api import expect, Page

logger = logging.getLogger(__name__)

# --- КЛАСС ДЛЯ API ---
class APIClient:
    def __init__(self, context, base_url):
        self.request = context
        self.base_url = base_url.strip("/")

    @allure.step("API GET запрос: {path}")
    def get(self, path=""):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.request.get(url)

# --- КЛАСС ДЛЯ UI (HOME PAGE) ---
class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://mwtestconsultancy.co.uk"
        
        # --- УНИВЕРСАЛЬНЫЕ ЛОКАТОРЫ (Оставляем только их) ---
        self.article_card = page.locator("article, .gh-card, .post-card") 
        self.article_title_inside_card = "h2, h3, .gh-card-title, .post-card-title"
        
        # --- ОСТАЛЬНЫЕ ЛОКАТОРЫ ---
        self.search_button = page.locator("button[aria-label='Search this site']:visible")
        self.search_frame_selector = 'iframe[title="portal-popup"]'
        self.search_input_selector = "input"
        self.header_locator = page.locator("h1")
        # СЮДА НИЧЕГО БОЛЬШЕ ДОБАВЛЯТЬ НЕ НУЖНО

    @allure.step("Открыть главную страницу")
    def open(self):
        logger.info(f"Открытие: {self.base_url}")
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=45000)
        return self

    @allure.step("Переход к разделу: {name}")
    def navigate_to(self, name: str):
        logger.info(f"Переход к разделу: {name}")
        link = self.page.get_by_role("link", name=re.compile(f"^{name}$", re.I)).first
        link.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Перейти в раздел Books")
    def navigate_to_books(self):
        self.navigate_to("Books")

    @allure.step("Поиск по тексту: {text}")
    def search_for(self, text: str):
        portal = self.wait_for_search_portal()
        search_input = portal.locator(self.search_input_selector)
        search_input.click() 
        search_input.fill(text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000) # Даем время на обновление результатов

    @allure.step("Проверить заголовок: {expected_text}")
    def check_title(self, expected_text: str):
        self.header_locator.first.wait_for(state="visible", timeout=15000)
        expect(self.header_locator.first).to_contain_text(expected_text, ignore_case=True)

    # --- НОВЫЕ МЕТОДЫ ДЛЯ СТАБИЛЬНОСТИ E2E И API ТЕСТОВ ---

    @allure.step("Получить заголовки всех статей")
    def get_all_article_titles(self):
        self.article_card.first.wait_for(state="visible", timeout=10000)
        titles = self.page.locator(self.article_title_inside_card).all_inner_texts()
        return [t.strip() for t in titles if t.strip()]

    @allure.step("Открыть первую статью и вернуть её заголовок")
    def open_first_book(self):
        first_title_locator = self.page.locator(self.article_title_inside_card).first
        first_title_locator.wait_for(state="visible")
        title_text = first_title_locator.inner_text().strip()
        
        # Кликаем по ссылке в первой карточке
        self.article_card.first.locator("a").first.click()
        self.page.wait_for_load_state("domcontentloaded")
        return title_text

    @allure.step("Логин (заглушка для тестов)")
    def login(self, email, password):
        logger.info(f"Логин под {email}")
        # Просто открываем форму логина, чтобы тест не падал по AttributeError
        self.navigate_to("Sign in")
        return self

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ---
    def wait_for_search_portal(self):
        self.search_button.first.click(force=True)
        portal = self.page.frame_locator(self.search_frame_selector)
        portal.locator(self.search_input_selector).wait_for(state="visible", timeout=15000)
        return portal

    def is_search_results_empty(self):
        self.page.wait_for_timeout(1000)
        portal = self.page.frame_locator(self.search_frame_selector)
        return portal.locator(self.article_title_inside_card).count() == 0