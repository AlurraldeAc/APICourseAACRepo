import logging

import pytest

from config.config import URL_GOREST
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

@pytest.fixture()
def create_user():
    user_id = None
    rest_client = RestClient()
    LOGGER.info("Fixture: Create a new user (init user)")
    body_request = {
        "name": "Marco Fio",
        "email": "marcofio@mail.com",
        "gender": "male",
        "status": "active"
    }
    url_gorest_users = f"{URL_GOREST}/users"
    response = rest_client.request("post", url_gorest_users, body=body_request)
    if response.status_code == 201:
        user_id = response.json()["id"]

    return user_id
