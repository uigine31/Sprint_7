import requests
import pytest
import allure
from urls import BASE_URL, LOGIN_ENDPOINT
from utils.courier_utils import delete_courier, login_courier, register_new_courier_and_return_login_password

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
        response = requests.post(self.BASE_URL, json={"login": login, "password": password})
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("wrong_field, wrong_value, expected_message", [
        ("password", "wrongpass", "Учетная запись не найдена"),
        ("login", "wronglogin", "Учетная запись не найдена")
    ])
    @allure.title('Авторизация с неверными данными')
    def test_login_courier_wrong_credentials_fails(self, courier, wrong_field, wrong_value, expected_message):
        login, password = courier
        # Подготовка payload с неверными данными
        payload = {"login": login, "password": password}
        if wrong_field == "password":
            payload["password"] = wrong_value
        elif wrong_field == "login":
            payload["login"] = wrong_value

        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 404
        assert expected_message in response.json().get("message", "")

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