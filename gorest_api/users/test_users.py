import logging

import pytest

from entities.user import User
from helpers.rest_client import RestClient
from config.config import URL_GOREST
from helpers.validate_response import ValidateResponse
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
        cls.validate = ValidateResponse()
        cls.user = User()

    @pytest.mark.acceptance
    def test_get_all_users(self, log_test_names):
        """
        Test get all user from GET endpoint
        """
        LOGGER.info("Test GET all users")
        response = self.user.get_all_users()
        self.validate.validate_response(response, "users", "Get_all_users")

    @pytest.mark.sanity
    def test_get_user(self, log_test_names):
        """
        Test get a specific user from GET endpoint
        """
        LOGGER.info("Test GET a user by Id")
        response = self.user.get_user(self.user_id)
        self.validate.validate_response(response, "users", "Get_user")

    @pytest.mark.acceptance
    def test_create_user(self, log_test_names):
        """
        Test create a new user (posts method)
        """
        LOGGER.info("Test create new user")
        response, _ = self.user.create_user()
        if response["status_code"] == 201:
            self.user_created_list.append(response["body"]["id"])
        self.validate.validate_response(response, "users", "Create_user")

    @pytest.mark.acceptance
    def test_update_user(self, log_test_names):
        """
        Test update user (the last created)
        """
        LOGGER.info("Test update user")
        create_response, _ = self.user.create_user()
        update_response = self.user.update_user(create_response)

        if update_response["status_code"] == 200:
            self.user_created_list.append(update_response["body"]["id"])
        self.validate.validate_response(update_response, "users", "Update_user")

    @pytest.mark.acceptance
    def test_delete_user(self, log_test_names):
        """
        Test delete a user
        """
        LOGGER.info("Test delete user")
        create_response, _ = self.user.create_user()
        response = self.user.delete_user(create_response["body"]["id"])
        self.validate.validate_response(response, "users", "Delete_user")

    @pytest.mark.negative
    def test_required_field_name(self, log_test_names):
        """
        Test required field is not sent in request body (name)
        """
        LOGGER.info("Test required field: name")
        response = self.user.create_missing_name()
        self.validate.validate_response(response, "users", "Name_required")

    @pytest.mark.negative
    def test_email_already_taken(self, log_test_names):
        """
        Test email address is already taken
        """
        LOGGER.info("Test email address is already taken")
        response_create, _ = self.user.create_user()
        if response_create["status_code"] == 201:
            self.user_created_list.append(response_create["body"]["id"])
        response = self.user.already_taken_email(response_create)
        self.validate.validate_response(response, "users", "eMail_already_taken")

    @pytest.mark.negative
    def test_nonexistent_user(self, log_test_names):
        """
        Test trying to retrieve a user that does not exist
        """
        LOGGER.info("Test retrieve user when resource is not available")
        user_id = 9999999
        response = self.user.get_user(user_id)
        self.validate.validate_response(response, "users", "Nonexistent_user")

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
