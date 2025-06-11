import requests
import pytest
import allure
from urls import BASE_URL, COURIER_ENDPOINT
from data.test_data import TEST_COURIER_DATA, EXPECTED_STATUS_DUPLICATE_COURIER, EXPECTED_MESSAGE_DUPLICATE_COURIER, EXPECTED_STATUS_MISSING_FIELDS_COURIER, EXPECTED_MESSAGE_MISSING_FIELDS_COURIER
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

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self, courier):
        login, password = courier
        payload = TEST_COURIER_DATA.copy()  # Используем копию
        payload.update({"login": login, "password": password})
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == EXPECTED_STATUS_DUPLICATE_COURIER
        assert EXPECTED_MESSAGE_DUPLICATE_COURIER in response.json().get("message", "")

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_fails(self, courier):
        login, password = courier
        payload = TEST_COURIER_DATA.copy()  # Используем копию
        payload.update({"login": login, "password": password})
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == EXPECTED_STATUS_DUPLICATE_COURIER
        assert EXPECTED_MESSAGE_DUPLICATE_COURIER in response.json().get("message", "")

    @allure.title('Все обязательные поля нужны для создания курьера')
    def test_create_courier_missing_fields_fails(self, courier):
        login, password = courier

        # Без login
        payload = TEST_COURIER_DATA.copy()
        payload.pop("login")
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == EXPECTED_STATUS_MISSING_FIELDS_COURIER
        assert EXPECTED_MESSAGE_MISSING_FIELDS_COURIER in response.json().get("message", "")

        # Без password
        payload = TEST_COURIER_DATA.copy()
        payload.pop("password")
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == EXPECTED_STATUS_MISSING_FIELDS_COURIER
        assert EXPECTED_MESSAGE_MISSING_FIELDS_COURIER in response.json().get("message", "")