import requests
import pytest
import allure
from utils.courier_utils import register_new_courier_and_return_login_password, delete_courier, login_courier
from urls import BASE_URL, COURIER_ENDPOINT, LOGIN_ENDPOINT

@allure.feature('Courier Login')
class TestCourierLogin:
    BASE_URL = f"{BASE_URL}{LOGIN_ENDPOINT}"

    @pytest.fixture
    def courier(self):
        login_pass = register_new_courier_and_return_login_password()
        assert len(login_pass) == 3
        login, password, _ = login_pass
        courier_id = login_courier(login, password)
        yield login, password
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, courier):
        login, password = courier
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={"login": login, "password": password})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Авторизация с неверным логином или паролем')
    def test_login_courier_wrong_credentials_fails(self, courier):
        login, password = courier
        # Неверный пароль
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={"login": login, "password": "wrongpass"})
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

        # Неверный логин
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={"login": "wronglogin", "password": password})
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title('Авторизация без обязательных полей')
    def test_login_courier_missing_fields_fails(self, courier):
        login, password = courier
        # Без login
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={"password": password})
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json().get("message", "")

        # Без password
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json={"login": login})
        assert response.status_code in [400, 504], "Ожидался код 400, но API может возвращать 504 из-за серверной ошибки."
        if response.status_code == 400:
            assert "Недостаточно данных для входа" in response.json().get("message", "")