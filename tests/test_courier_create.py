import requests
import pytest
import allure
from urls import BASE_URL, COURIER_ENDPOINT
from data.test_data import TEST_COURIER_DATA, EXPECTED_STATUS_DUPLICATE_COURIER, EXPECTED_MESSAGE_DUPLICATE_COURIER, EXPECTED_STATUS_MISSING_FIELDS_COURIER, EXPECTED_MESSAGE_MISSING_FIELDS_COURIER
import random
import string

from utils.courier_utils import delete_courier, login_courier, register_new_courier_and_return_login_password

@allure.feature('Courier Creation')
class TestCourierCreate:
    BASE_URL = f"{BASE_URL}{COURIER_ENDPOINT}"

    @pytest.fixture
    def courier(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3, "Курьер не создан"
        login, password, _ = login_pass
        courier_id = login_courier(login, password)
        yield login, password
        if courier_id:
            delete_courier(courier_id)

    def generate_unique_login(self, length=10):
        """Генерирует уникальный логин."""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        unique_login = self.generate_unique_login()
        payload = TEST_COURIER_DATA.copy()
        payload.update({
            "login": unique_login,
            "password": "test_password123",  # Используем фиксированный пароль для теста
            "firstName": "TestUser"
        })
        with allure.step(f"Отправка запроса на создание нового курьера с данными: {payload}"):
            response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 201
        assert response.json().get("ok") is True

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, courier):
        login, password = courier
        payload = TEST_COURIER_DATA.copy()
        payload.update({"login": login, "password": password})
        with allure.step(f"Отправка запроса на создание дубликата курьера с данными: {payload}"):
            response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == EXPECTED_STATUS_DUPLICATE_COURIER
        assert EXPECTED_MESSAGE_DUPLICATE_COURIER in response.json().get("message", "")

    @pytest.mark.parametrize("test_name, payload", [
        ("missing_login", lambda login, password: {"password": password, "firstName": "Test"}),
        ("missing_password", lambda login, password: {"login": login, "firstName": "Test"})
    ])
    @allure.title('Создание курьера без обязательного поля')
    def test_create_courier_missing_field_fails(self, courier, test_name, payload):
        login, password = courier
        # Вычисляем payload с реальными данными из фикстуры
        updated_payload = payload(login, password)
        with allure.step(f"Отправка запроса на создание курьера без поля ({test_name}): {updated_payload}"):
            response = requests.post(self.BASE_URL, json=updated_payload)
        assert response.status_code == EXPECTED_STATUS_MISSING_FIELDS_COURIER
        assert EXPECTED_MESSAGE_MISSING_FIELDS_COURIER in response.json().get("message", "")