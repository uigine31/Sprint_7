import pytest
from utils.courier_utils import register_new_courier_and_return_login_password, delete_courier, login_courier

@pytest.fixture
def courier():
    login_pass = register_new_courier_and_return_login_password()
    assert len(login_pass) == 3, "Курьер не создан"
    login, password, _ = login_pass
    courier_id = login_courier(login, password)
    yield login, password
    if courier_id:
        delete_courier(courier_id)