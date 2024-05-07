import logging

import pytest

from entities.post import Post
from entities.user import User
from helpers.rest_client import RestClient
from config.config import URL_GOREST
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestPosts:
    url_gorest_posts = None
    rest_client = None
    post_created_list = None
    post_id = None

    @classmethod
    def setup_class(cls):
        """
        Setup class for posts
        """
        cls.rest_client = RestClient()
        cls.url_gorest_posts = f"{URL_GOREST}/posts"
        response = cls.rest_client.request("get", cls.url_gorest_posts)
        cls.post_id = response["body"][0]["id"]
        LOGGER.debug("Post Id: %s", cls.post_id)
        cls.post_created_list = []
        cls.validate = ValidateResponse()
        cls.user = User()
        cls.post = Post()

    @pytest.mark.acceptance
    def test_get_all_posts(self, log_test_names):
        """
        Test get all posts from GET endpoint
        """
        LOGGER.info("Test GET all posts")
        response = self.post.get_all_post()
        self.validate.validate_response(response, "posts", "Get_all_posts")

    @pytest.mark.acceptance
    def test_get_post(self, log_test_names):
        """
        Test get a specific post object from GET endpoint
        """
        LOGGER.info("Test GET a post by Id")
        response = self.post.get_post(self.post_id)
        self.validate.validate_response(response, "posts", "Get_post")

    @pytest.mark.acceptance
    def test_create_post(self, log_test_names):
        """
        Test create a new post object (posts method)
        """
        LOGGER.info("Test create new post")
        create_response = self.user.create_user()
        response = self.post.create_post(create_response["body"]["id"])
        if response["status_code"] == 201:
            self.post_created_list.append(response["body"]["id"])
        self.validate.validate_response(response, "posts", "Create_post")

    @pytest.mark.acceptance
    def test_update_post(self, log_test_names):
        """
        Test update post object (the last created)
        """
        LOGGER.info("Test update posts")
        create_response = self.user.create_user()
        create_post_response = self.post.create_post(create_response["body"]["id"])
        update_response = self.post.update_post(create_post_response)
        if update_response["status_code"] == 200:
            self.post_created_list.append(update_response["body"]["id"])
        self.validate.validate_response(update_response, "posts", "Update_post")

    @pytest.mark.acceptance
    def test_delete_post(self, log_test_names):
        """
        Test delete a post
        """
        LOGGER.info("Test delete post object")
        create_response = self.user.create_user()
        create_post_response = self.post.create_post(create_response["body"]["id"])
        delete_response = self.post.delete_post(create_post_response["body"]["id"])
        self.validate.validate_response(delete_response, "posts", "Delete_post")

    @pytest.mark.negative
    def test_required_title(self, log_test_names):
        """
        Test title required field is not sent in request body
        """
        LOGGER.info("Test required field: title in post")
        response = self.post.create_missing_title()
        self.validate.validate_response(response, "posts", "Field_required")

    @pytest.mark.negative
    def test_required_body(self, log_test_names):
        """
        Test body required field is not sent in request body
        """
        LOGGER.info("Test required field: 'Body' content in post")
        response = self.post.create_missing_post_body()
        self.validate.validate_response(response, "posts", "Field_required")

    @pytest.mark.negative
    def test_nonexistent_post(self, log_test_names):
        """
        Test trying to retrieve a post object that does not exist
        """
        LOGGER.info("Test retrieve user when resource is not available")
        post_id = 9999999999
        response = self.post.get_post(post_id)
        self.validate.validate_response(response, "posts", "Non_existent_post")

# This teardown class method would be unnecessary if the "test_create_user" test
# were not leaving single user alone that it not being deleted after all tests.
    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup posts data")
        for post_id in cls.post_created_list:
            url_delete_post = f"{cls.url_gorest_posts}/{post_id}"
            response = cls.rest_client.request("delete", url_delete_post)
            if response["status_code"] == 204:
                LOGGER.info("Deleted posts Id:  %s", post_id)
