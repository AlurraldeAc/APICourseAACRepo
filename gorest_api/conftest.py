"""
Confing test file pytest
"""
import logging
import pytest

from entities.post import Post
from entities.user import User
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_user():
    """
    Create user method
    Returns:

    """
    user_id = None
    LOGGER.info("Fixture: Create a new user (init user)")
    user_object = User()
    response, rest_client = user_object.create_user()
    if response["status_code"] == 201:
        user_id = response["body"]["id"]

    yield user_id
    LOGGER.debug("Yield fixture: delete the just created user from conftest.py")
    delete_user(user_id, user_object)
    # return user_id
    # instead of return applying Yield fixture: So, creates user. Return Id, then run the test,
    # and comes back to Yield and executes the rest of the code (deleting the created user).


@pytest.fixture()
def create_post(user_id):
    """
    Create post
    Args:
        user_id:

    Returns:

    """
    post_id = None
    LOGGER.info("Test create post")
    post_object = Post()
    response = post_object.create_post(user_id)
    if response.status_code == 201:
        post_id = response.json()["id"]
    return post_id


# Now, yield will call delete_user(user_id, user_object) method.
def delete_user(user_id, user_object):
    """
    Delete user
    Args:
        user_id:
        user_object:

    Returns:

    """
    user_object.delete_user(user_id)


# This fixture is useful to delimit the Start and End of a test.
# First line will be print at the beginning od the test. The second one at the end of the test.
# The log_test_names sent as parameter in tests method - It retrieves the test name and prints it.
@pytest.fixture()
def log_test_names(request):
    """
    Log test ini : title test
    Args:
        request:

    Returns:

    """
    LOGGER.info("****** Test '%s' STARTED ******", request.node.name)

    def ending_test_info():
        """
        Log test ending info
        Returns:

        """
        LOGGER.info("------ Test '%s' COMPLETED ------\n", request.node.name)

    request.addfinalizer(ending_test_info)
