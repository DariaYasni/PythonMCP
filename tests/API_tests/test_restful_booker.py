import pytest
import allure
import time
from pydantic import BaseModel
from typing import Optional


# 1. Вставляем схему прямо сюда, чтобы не было проблем с импортом
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


@allure.feature("Restful Booker API")
class TestBookerAPI:

    @allure.story("1. Health Check")
    def test_api_ping(self, booker_api):
        response = booker_api.get("/ping")
        # API иногда возвращает 201, иногда 200. Проверим оба варианта.
        assert response.status in [200, 201]

    @allure.story("2. Contract Validation")
    def test_booking_headers(self, booker_api):
        response = booker_api.get("/booking")
        assert "application/json" in response.headers.get("content-type", "")
        assert response.status == 200

    @allure.story("3. Performance")
    def test_api_performance(self, booker_api):
        start = time.time()
        booker_api.get("/booking")
        duration = (time.time() - start) * 1000
        assert duration < 5000, f"API медленное: {duration:.2f}ms"

    @allure.story("4. Data Integrity")
    def test_data_structure(self, booker_api):
        response = booker_api.get("/booking")
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "bookingid" in data[0]

    @allure.story("5. E2E: Create and Verify with Pydantic")
    def test_create_booking_e2e(self, booker_api):
        payload = {
            "firstname": "MidLevel",
            "lastname": "QA",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
            "additionalneeds": "Breakfast",
        }
        res = booker_api.post("/booking", data=payload)
        assert res.status == 200

        booking_data = res.json()["booking"]
        # Валидация через схему, которую мы вставили выше
        validated_booking = BookingModel(**booking_data)

        assert validated_booking.firstname == "MidLevel"
        assert validated_booking.lastname == "QA"

        booking_id = res.json()["bookingid"]
        assert isinstance(booking_id, int)

    @allure.story("6. Data Driven Testing")
    @pytest.mark.parametrize("firstname", ["Sally", "Jim"])
    def test_filter_by_name(self, booker_api, firstname):
        response = booker_api.get(f"/booking?firstname={firstname}")
        assert response.status == 200
        assert isinstance(response.json(), list)
