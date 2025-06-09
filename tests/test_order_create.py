import requests
import pytest
import allure
from data.test_data import ORDER_DATA, COLOR_VARIATIONS

@allure.feature('Order Creation')
class TestOrderCreate:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Создание заказа с разными цветами: {color}')
    @pytest.mark.parametrize('color', COLOR_VARIATIONS)
    def test_create_order_with_different_colors(self, color):
        order_data = ORDER_DATA.copy()
        order_data["color"] = color[0]

        response = requests.post(self.BASE_URL, json=order_data)
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        assert "track" in response.json(), "В ответе отсутствует поле track"