class APIClient:
    def __init__(self, context):
        # Обязательно двойные подчеркивания по бокам и знак равно
        self.request = context
        # Используем полный адрес сайта
        self.base_url = "https://mwtestconsultancy.co.uk" 

    def get_main_page(self):
        """Метод для получения главной страницы"""
        return self.request.get(self.base_url)

    def check_page_content(self):
        """Метод для проверки контента (через эндпоинт /)"""
        return self.request.get(f"{self.base_url}/")