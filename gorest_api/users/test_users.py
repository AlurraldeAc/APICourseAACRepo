import logging

from helpers.rest_client import RestClient
from config.config import URL_GOREST
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestUsers:
    @classmethod
    def setup_class(cls):
        """
        Setup class for users
        """
        cls.rest_client = RestClient()
        cls.url_gorest_users = f"{URL_GOREST}/users"
        response = cls.rest_client.request("get", cls.url_gorest_users)
        cls.user_id = response["body"][0]["id"]
        LOGGER.debug("User Id: %s", cls.user_id)
        cls.user_created_list = []

    def test_get_all_users(self, log_test_names):
        """
        Test get all user from GET endpoint
        """
        LOGGER.info("Test GET all users")
        response = self.rest_client.request("get", self.url_gorest_users)
        # From assert response.status_code == 200  --> assert response["status_code"]== 200
        # To
        assert response["status_code"] == 200

    def test_get_user(self, log_test_names):
        """
        Test get a specific user from GET endpoint
        """
        LOGGER.info("Test GET a user by Id")
        url_get_user = f"{self.url_gorest_users}/{self.user_id}"
        response = self.rest_client.request("get", url_get_user)
        assert response["status_code"] == 200

    def test_create_user(self, log_test_names):
        """
        Test create a new user (post method)
        """
        LOGGER.info("Test create new user")
        body_request = {
            "name": "Rolando Bladez",
            "email": "blrol@mail.com",
            "gender": "male",
            "status": "active"
        }
        response = self.rest_client.request("post", self.url_gorest_users, body=body_request)
        if response["status_code"] == 201:
            self.user_created_list.append(response["body"]["id"])

        assert response["status_code"] == 201

    def test_update_user(self, create_user, log_test_names):
        """
        Test update user (the last created)
        """
        LOGGER.info("Test update user")
        url_update_user = f"{self.url_gorest_users}/{create_user}"
        body_request_update = {
            "name": "Marco Fio",
            "email": "markCleo@mail.com",
            "gender": "male",
            "status": "inactive"
        }
        LOGGER.info("User to update, %s", self.user_id)
        response = self.rest_client.request("put", url_update_user, body=body_request_update)
        if response["status_code"] == 200:
            self.user_created_list.append(response["body"]["id"])
        assert response["status_code"] == 200

    def test_delete_user(self, create_user, log_test_names):
        """
        Test delete a user
        """
        LOGGER.info("Test delete user")
        url_delete_user = f"{self.url_gorest_users}/{create_user}"
        LOGGER.info("user Id to be deleted : %s", create_user)
        response = self.rest_client.request("delete", url_delete_user)
        assert response["status_code"] == 204

# This teardown class method would be unnecessary if the "test_create_user" test
# were not leaving single user alone that it not being deleted after all tests.
    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup users data")
        for user_id in cls.user_created_list:
            url_delete_user = f"{cls.url_gorest_users}/{user_id}"
            response = cls.rest_client.request("delete", url_delete_user)
            if response["status_code"] == 204:
                LOGGER.info("project Id deleted : %s", user_id)
