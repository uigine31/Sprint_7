# data/test_data.py
# Данные для создания заказа
ORDER_DATA = {
    "firstName": "Test",
    "lastName": "User",
    "address": "123 Street",
    "metroStation": 1,
    "phone": "+79991234567",
    "rentTime": 1,
    "deliveryDate": "2025-06-07",
    "comment": "Test order",
    "color": ["BLACK"]
}

# Варианты цветов для параметризации
COLOR_VARIATIONS = [
    (["BLACK"],),
    (["GREY"],),
    (["BLACK", "GREY"],),
    ([],)
]

# Данные для создания курьера
TEST_COURIER_DATA = {
    "login": "test_login",
    "password": "test_password",
    "firstName": "Test"
}

# Ожидаемые ответы для создания курьера
EXPECTED_STATUS_DUPLICATE_COURIER = 409
EXPECTED_MESSAGE_DUPLICATE_COURIER = "Этот логин уже используется"
EXPECTED_STATUS_MISSING_FIELDS_COURIER = 400
EXPECTED_MESSAGE_MISSING_FIELDS_COURIER = "Недостаточно данных для создания учетной записи"