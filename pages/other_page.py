from playwright.sync_api import Page

class ContactPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = 'https://www.mwtestconsultancy.co.uk/contact'

    def load(self):
        """Загружает страницу 'Contact Us'."""
        self.page.goto(self.url)

    def fill_name(self, name: str):
        """Заполняет поле для имени."""
        self.page.fill('input[name="name"]', name)

    def fill_email(self, email: str):
        """Заполняет поле для email."""
        self.page.fill('input[name="email"]', email)

    def fill_message(self, message: str):
        """Заполняет поле для сообщения."""
        self.page.fill('textarea[name="message"]', message)

    def submit_form(self):
        """Отправляет форму."""
        self.page.click('button[type="submit"]')

    def is_confirmation_visible(self) -> bool:
        """Проверяет, появилась ли на странице форма подтверждения отправки."""
        return self.page.is_visible('div.confirmation-message')