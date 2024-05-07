import logging

import pytest

from entities.todo import Todo
from entities.user import User
from helpers.rest_client import RestClient
from config.config import URL_GOREST
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestTodos:
    rest_client = None
    url_gorest_todos = None
    todo_created_list = None
    todo_id = None

    @classmethod
    def setup_class(cls):
        """
        Setup class for todos
        """
        cls.rest_client = RestClient()
        cls.url_gorest_todos = f"{URL_GOREST}/todos"
        response = cls.rest_client.request("get", cls.url_gorest_todos)
        cls.todo_id = response["body"][0]["id"]
        LOGGER.debug("Todo Id: %s", cls.todo_id)
        cls.todo_created_list = []
        cls.validate = ValidateResponse()
        cls.user = User()
        cls.todo = Todo()

    @pytest.mark.acceptance
    def test_get_all_todos(self, log_test_names):
        """
        Test get all todos from GET endpoint
        """
        LOGGER.info("Test GET all todos")
        response = self.todo.get_all_todos()
        self.validate.validate_response(response, "todos", "Get_all_todos")

    @pytest.mark.acceptance
    def test_get_todo(self, log_test_names):
        """
        Test get a specific todos object from GET endpoint
        """
        LOGGER.info("Test GET a todo by Id")
        response = self.todo.get_todo(self.todo_id)
        self.validate.validate_response(response, "todos", "Get_todo")

    @pytest.mark.acceptance
    def test_create_todo(self, log_test_names):
        """
        Test create a new todo_object (posts method)
        """
        LOGGER.info("Test create new todo")
        create_response = self.user.create_user()
        response = self.todo.create_todo(create_response["body"]["id"])
        if response["status_code"] == 201:
            self.todo_created_list.append(response["body"]["id"])
        self.validate.validate_response(response, "todos", "Create_todo")

    @pytest.mark.acceptance
    def test_update_todo(self, log_test_names):
        """
        Test update todo_object (the last created)
        """
        LOGGER.info("Test update todo")
        create_response = self.user.create_user()
        create_todo_response = self.todo.create_todo(create_response["body"]["id"])
        update_response = self.todo.update_todo(create_todo_response)
        if update_response["status_code"] == 200:
            self.todo_created_list.append(update_response["body"]["id"])
        self.validate.validate_response(update_response, "todos", "Update_todo")

    @pytest.mark.acceptance
    def test_delete_todo(self, log_test_names):
        """
        Test delete a todo_object
        """
        LOGGER.info("Test delete todo")
        create_response = self.user.create_user()
        create_todo_response = self.todo.create_todo(create_response["body"]["id"])
        delete_response = self.todo.delete_todo(create_todo_response["body"]["id"])
        self.validate.validate_response(delete_response, "todos", "Delete_todo")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup todos data")
        for todo_id in cls.todo_created_list:
            url_delete_todo = f"{cls.url_gorest_todos}/{todo_id}"
            response = cls.rest_client.request("delete", url_delete_todo)
            if response["status_code"] == 204:
                LOGGER.info("Todos deleted Id: %s", todo_id)
