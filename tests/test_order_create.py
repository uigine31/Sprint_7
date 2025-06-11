import requests
import pytest
import allure
from urls import BASE_URL, ORDERS_ENDPOINT
from data.test_data import ORDER_DATA, COLOR_VARIATIONS

@allure.feature('Order Creation')
class TestOrderCreate:
    BASE_URL = f"{BASE_URL}{ORDERS_ENDPOINT}"

    @pytest.mark.parametrize('color', COLOR_VARIATIONS)
    @allure.title('Создание заказа с разными цветами')
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_DATA.copy()
        payload.update({"color": color[0]})  # Извлекаем первый элемент кортежа
        with allure.step(f"Отправка запроса на создание заказа с данными: {payload}"):
            response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()