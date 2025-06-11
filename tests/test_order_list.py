import requests
import pytest
import allure
from urls import BASE_URL, ORDERS_ENDPOINT

@allure.feature('Order List')
class TestOrderList:
    BASE_URL = f"{BASE_URL}{ORDERS_ENDPOINT}"

    @allure.title('Получение списка заказов')
    def test_get_order_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(self.BASE_URL)
        assert response.status_code == 200
        assert "orders" in response.json()