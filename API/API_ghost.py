import os
from dotenv import load_dotenv

load_dotenv()


class GhostClient:
    def __init__(self, context):
        self.request = context
        self.base_url = os.getenv("GHOST_URL")
        self.api_key = os.getenv("GHOST_KEY")

    def get_settings(self):
        """Проверка мета-данных блога (Read-only)"""
        return self.request.get(
            f"{self.base_url}/settings/", params={"key": self.api_key}
        )

    def get_all_posts(self):
        """Получение всех статей для проверки контента"""
        return self.request.get(f"{self.base_url}/posts/", params={"key": self.api_key})

    def get_posts_unauthorized(self):
        """НЕГАТИВНЫЙ ТЕСТ: Проверка защиты бэкенда"""
        return self.request.get(f"{self.base_url}/posts/", params={"key": "WRONG_KEY"})
