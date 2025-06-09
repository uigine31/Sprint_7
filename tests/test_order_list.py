import requests
import pytest
import allure

@allure.feature('Order List')
class TestOrderList:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Получение списка заказов')
    def test_get_order_list(self):
        response = requests.get(self.BASE_URL)
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)