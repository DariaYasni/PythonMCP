from pydantic import BaseModel, Field
from typing import Optional


# Описываем, как должны выглядеть даты
class BookingDates(BaseModel):
    checkin: str
    checkout: str


# Описываем структуру одного бронирования
class BookingModel(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None  # Это поле может отсутствовать
