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
        payload = {"login": login, "password": password}
        with allure.step(f"Отправка запроса на авторизацию курьера с данными: {payload}"):
            response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("test_case, payload, expected_message", [
        ("wrong_password", lambda login, password: {"login": login, "password": "wrongpass"}, "Учетная запись не найдена"),
        ("wrong_login", lambda login, password: {"login": "wronglogin", "password": password}, "Учетная запись не найдена")
    ])
    @allure.title('Авторизация с неверными данными')
    def test_login_courier_wrong_credentials_fails(self, courier, test_case, payload, expected_message):
        login, password = courier
        # Вычисляем payload с реальными данными из фикстуры
        updated_payload = payload(login, password)
        with allure.step(f"Отправка запроса на авторизацию с неверным {test_case}: {updated_payload}"):
            response = requests.post(self.BASE_URL, json=updated_payload)
        assert response.status_code == 404
        assert expected_message in response.json().get("message", "")

    @pytest.mark.parametrize("test_case, payload", [
        ("missing_login", lambda login, password: {"password": password}),
        ("missing_password", lambda login, password: {"login": login})
    ])
    @allure.title('Авторизация без обязательного поля')
    def test_login_courier_missing_field_fails(self, courier, test_case, payload):
        login, password = courier
        # Вычисляем payload с реальными данными из фикстуры
        updated_payload = payload(login, password)
        with allure.step(f"Отправка запроса на авторизацию без поля {test_case}: {updated_payload}"):
            response = requests.post(self.BASE_URL, json=updated_payload)
        expected_status = [400, 504]
        assert response.status_code in expected_status, f"Ожидался код 400 или 504, получен {response.status_code}"
        if response.status_code == 400:
            assert "Недостаточно данных для входа" in response.json().get("message", "")