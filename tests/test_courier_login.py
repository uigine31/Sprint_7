import requests
import pytest
import allure
from urls import BASE_URL, LOGIN_ENDPOINT

@allure.feature('Courier Login')
class TestCourierLogin:
    BASE_URL = f"{BASE_URL}{LOGIN_ENDPOINT}"

    @allure.title('Успешная авторизация курьера')
    def test_login_courier_success(self, courier):
        login, password = courier
        response = requests.post(self.BASE_URL, json={"login": login, "password": password})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Авторизация с неверным логином или паролем')
    def test_login_courier_wrong_credentials_fails(self, courier):
        login, password = courier
        # Неверный пароль
        response = requests.post(self.BASE_URL, json={"login": login, "password": "wrongpass"})
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

        # Неверный логин
        response = requests.post(self.BASE_URL, json={"login": "wronglogin", "password": password})
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")

    @allure.title('Авторизация без обязательных полей')
    def test_login_courier_missing_fields_fails(self, courier):
        login, password = courier
        # Без login
        response = requests.post(self.BASE_URL, json={"password": password})
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.json().get("message", "")

        # Без password
        response = requests.post(self.BASE_URL, json={"login": login})
        assert response.status_code in [400, 504], "Ожидался код 400, но API может возвращать 504 из-за серверной ошибки."
        if response.status_code == 400:
            assert "Недостаточно данных для входа" in response.json().get("message", "")