import requests
import pytest
import allure
from urls import BASE_URL, ORDERS_ENDPOINT

@allure.feature('Order Creation')
class TestOrderCreate:
    BASE_URL = f"{BASE_URL}{ORDERS_ENDPOINT}"

    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title('Создание заказа с разными цветами')
    def test_create_order_with_different_colors(self, color):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Address",
            "metroStation": 1,
            "phone": "+79991234567",
            "rentTime": 1,
            "deliveryDate": "2025-06-11",
            "comment": "Test comment",
            "color": color
        }
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()