from pydantic import BaseModel, Field
from typing import Optional, List


# === МОДЕЛИ ДЛЯ BOOKING (Тренажер herokuapp) ===
class BookingDates(BaseModel):
    checkin: str
    checkout: str


class BookingModel(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


# === МОДЕЛИ ДЛЯ GHOST (Блог mwtestconsultancy) ===
# Добавляем их сюда же, чтобы фреймворк был полным
class GhostPostModel(BaseModel):
    id: str
    title: str
    url: str
    published_at: str


class GhostSettingsModel(BaseModel):
    title: str
    description: str
    navigation: List[dict]
