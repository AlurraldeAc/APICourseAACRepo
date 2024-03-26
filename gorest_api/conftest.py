import logging

import pytest
import requests

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

@pytest.fixture()
def create_user():
    user_id = None
    LOGGER.info("Fixture: Create a new user (init user)")
    body_request = {
        "name": "Marco Fio",
        "email": "marcofio@mail.com",
        "gender": "male",
        "status": "active"
    }
    token = "f4e20b30d371e2bf41c95716f0e33b90d84d0aeadb353811a199915e940bcc8a"
    url_gorest_users = "https://gorest.co.in/public/v2/users"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url_gorest_users, headers=headers, data=body_request)
    LOGGER.debug("Response to create project(json): %s", response.json())
    LOGGER.debug("Status Code: %s", response.status_code)
    if response.status_code == 201:
        user_id = response.json()["id"]

    return user_id
