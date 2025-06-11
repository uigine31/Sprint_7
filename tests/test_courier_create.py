import requests
import pytest
import allure
from urls import BASE_URL, COURIER_ENDPOINT

@allure.feature('Courier Creation')
class TestCourierCreate:
    BASE_URL = f"{BASE_URL}{COURIER_ENDPOINT}"

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self, courier):
        login, password = courier
        payload = {"login": login, "password": password, "firstName": "Test"}
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется. Попробуйте другой." in response.json().get("message", "")

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, courier):
        login, password = courier
        payload = {"login": login, "password": password, "firstName": "Test"}
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется. Попробуйте другой." in response.json().get("message", "")

    @allure.title('Все обязательные поля нужны для создания курьера')
    def test_create_courier_missing_fields_fails(self, courier):
        login, password = courier

        # Без login
        payload = {"password": password, "firstName": "Test"}
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "")

        # Без password
        payload = {"login": login, "firstName": "Test"}
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message", "")