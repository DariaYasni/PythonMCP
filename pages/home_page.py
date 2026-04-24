import re
import logging
from playwright.sync_api import expect, Page

logger = logging.getLogger(__name__)

# --- КЛАССЫ ДЛЯ API ---

class APIClient:
    def __init__(self, context, base_url):
        self.request = context
        self.base_url = base_url.strip("/")  # Убираем лишние слеши

    def get(self, path=""):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.request.get(url)

    def post(self, path="", data=None):
        """
        Отправляет POST запрос. 
        Используем аргумент 'data', но если передаем словарь, 
        Playwright отправит его как JSON.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.request.post(url, data=data)


class MainPage(APIClient):
    """Класс для API тестов"""
    def __init__(self, context, base_url):
        super().__init__(context, base_url)

    def get_main_page(self):
        return self.get()


# --- КЛАСС ДЛЯ UI (HOME PAGE) ---

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "https://mwtestconsultancy.co.uk"
        
        # --- ЛОКАТОРЫ ---
        self.search_button = page.locator("button[aria-label='Search this site']:visible")
        self.search_frame_selector = 'iframe[title="portal-popup"]'
        self.search_input_selector = "input"
        self.header_locator = page.locator("h1")
        self.article_card = page.locator("article.gh-card")
        self.article_title_inside_card = "h2, h3, .gh-card-title" 

    def open(self):
        logger.info(f"Открытие: {self.base_url}")
        try:
            self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=45000)
        except Exception as e:
            logger.warning(f"Сайт долго грузится, но мы продолжаем: {e}")
        
        # Ждем появления первой карточки, чтобы убедиться, что контент загружен
        try:
            self.article_card.first.wait_for(state="attached", timeout=15000)
        except:
            logger.warning("Карточки статей не найдены при загрузке")
        return self

    def navigate_to(self, name: str):
        logger.info(f"Переход к разделу: {name}")
        link = self.page.get_by_role("link", name=re.compile(f"^{name}$", re.I)).first
        link.click()
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_to_books(self):
        self.navigate_to("Books")

    def navigate_to_tools(self):
        self.navigate_to("Tools")

    def navigate_to_info_page(self, name="About"):
        self.navigate_to(name)

    def wait_for_search_portal(self):
        logger.info("Открытие окна поиска...")
        self.search_button.first.click(force=True)
        portal = self.page.frame_locator(self.search_frame_selector)
        portal.locator(self.search_input_selector).wait_for(state="visible", timeout=15000)
        return portal

    def search_for(self, text: str):
        portal = self.wait_for_search_portal()
        search_input = portal.locator(self.search_input_selector)
        search_input.click() 
        search_input.fill(text)
        self.page.keyboard.press("Enter")
        try:
            self.page.wait_for_url(f"**/{text.lower()}/**", timeout=15000)
            self.page.wait_for_load_state("networkidle")
        except:
            logger.info("URL не изменился автоматически или страница грузится долго.")

    def get_no_results_message(self):
        portal = self.page.frame_locator(self.search_frame_selector)
        return portal.get_by_text(re.compile(r"No results", re.I))

    def get_all_article_titles(self):
        """Собирает заголовки статей. Работает и в поиске, и на главной."""
        if self.page.locator(self.search_frame_selector).is_visible():
            portal = self.page.frame_locator(self.search_frame_selector)
            return portal.locator(self.article_title_inside_card).all_inner_texts()
        
        # Собираем заголовки на обычной странице
        titles = self.page.locator(self.article_title_inside_card).all_inner_texts()
        # Очищаем от лишних пробелов и пустых строк
        return [t.strip() for t in titles if t.strip()]

    def check_title(self, expected_text: str):
        self.header_locator.first.wait_for(state="visible", timeout=15000)
        expect(self.header_locator.first).to_contain_text(expected_text, ignore_case=True)

    def open_first_book(self):
        self.article_card.first.wait_for(state="attached", timeout=10000)
        card = self.article_card.first
        card.scroll_into_view_if_needed()
        title_element = card.locator(self.article_title_inside_card).first
        title_element.wait_for(state="attached", timeout=10000)
        expected_title = title_element.inner_text().strip()
        logger.info(f"Кликаем по статье: {expected_title}")
        card.locator("a").first.click(force=True)
        return expected_title

    def is_search_results_empty(self):
        portal = self.page.frame_locator(self.search_frame_selector)
        count = portal.locator(self.article_title_inside_card).count()
        return count == 0