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

    yield user_id
    LOGGER.debug("Yield fixture: delete the just created user from conftest.py")
    delete_user(user_id, rest_client)
    # return user_id
    # instead of return applying Yield fixture: So, creates user. Return Id, then run the test,
    # and comes back to Yield and executes the rest of the code (deleting the created user).


# Now, yield will call delete_project(project_id, rest_client) method.
def delete_user(user_id, rest_client):
    LOGGER.debug("Cleanup user")
    url_delete_project = f"{URL_GOREST}/users/{user_id}"
    response = rest_client.request("delete", url_delete_project)
    if response.status_code == 204:
        LOGGER.info("Deleted user Id : %s", user_id)

# This fixture is useful to delimit the Start and End of a test.
# First line will be print at the beginning od the test. The second one at the end of the test.
# The log_test_names sent as parameter in tests method - It retrieves the test name and prints it.
@pytest.fixture()
def log_test_names(request):
    LOGGER.info("****** Test '%s' STARTED ******", request.node.name)

    def ending_test_info():
        LOGGER.info("------ Test '%s' COMPLETED ------\n", request.node.name)
    request.addfinalizer(ending_test_info)
