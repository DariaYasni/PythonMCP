import os
from dotenv import load_dotenv

load_dotenv()


class BookerClient:
    def __init__(self, context):
        self.request = context
        self.base_url = os.getenv("BOOKER_URL")

    def create_token(self):
        """Получение токена (нужен для PUT/DELETE)"""
        payload = {"username": "admin", "password": "password123"}
        response = self.request.post(f"{self.base_url}/auth", data=payload)
        return response.json()["token"]

    def create_booking(self, booking_data):
        """Создание бронирования (C из CRUD)"""
        return self.request.post(f"{self.base_url}/booking", data=booking_data)
