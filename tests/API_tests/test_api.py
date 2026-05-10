import pytest
import requests
import time


# 1. Health Check (Проверка доступности)
def test_api_ping_status(api_url):
    # Тело функции смещено на 4 пробела
    response = requests.get(f"{api_url}/ping")
    assert response.status_code == 201, "API тренажер недоступен"


# 2. Header & Contract Validation (Проверка контракта)
def test_get_booking_headers(api_url):
    response = requests.get(f"{api_url}/booking")
    assert "application/json" in response.headers.get("Content-Type", "")
    assert response.status_code == 200


# 3. Performance Test (SLA)
def test_api_performance(api_url):
    start_time = time.time()
    requests.get(f"{api_url}/booking")
    duration_ms = (time.time() - start_time) * 1000
    assert duration_ms < 5000, f"API слишком медленное: {duration_ms:.2f}ms"


# 4. Data Integrity (Целостность данных)
def test_booking_ids_structure(api_url):
    response = requests.get(f"{api_url}/booking")
    data = response.json()
    assert isinstance(data, list), "Ожидался список бронирований"
    if len(data) > 0:
        # Уровень вложенности внутри if — еще 4 пробела
        assert "bookingid" in data[0]


# 5. E2E Scenario (Сквозной тест: Создание -> Проверка)
def test_create_and_verify_booking(api_url):
    booking_data = {
        "firstname": "MidLevel",
        "lastname": "QA",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
        "additionalneeds": "Breakfast",
    }
    create_res = requests.post(f"{api_url}/booking", json=booking_data)
    assert create_res.status_code == 200
    booking_id = create_res.json()["bookingid"]

    get_res = requests.get(f"{api_url}/booking/{booking_id}")
    assert get_res.json()["firstname"] == "MidLevel"


# 6. Data Driven Testing (Параметризация)
@pytest.mark.parametrize(
    "firstname, lastname", [("Sally", "Brown"), ("Jim", "Ericsson")]
)
def test_filter_bookings_by_name(api_url, firstname, lastname):
    url = f"{api_url}/booking?firstname={firstname}&lastname={lastname}"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
