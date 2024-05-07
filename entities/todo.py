import logging
import random

from datetime import datetime, timedelta
from config.config import URL_GOREST
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Todo:

    def __init__(self, rest_client=None):
        self.url_gorest_todos = f"{URL_GOREST}/todos"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_todo(self, user_id):
        number = random.randint(0, 999)
        next_day_timestamp = datetime.now() + timedelta(days=1)
        due_on = next_day_timestamp.isoformat()
        body_todo = {
            "user_id": f"{user_id}",
            "title": f"Todo object test {number}",
            "due_on": f"{due_on}",
            "status": "pending"
        }
        response = self.rest_client.request("post", self.url_gorest_todos, body=body_todo)
        return response

    def update_todo(self, todo_object):
        id_ = todo_object["body"]["id"]
        usr_id = todo_object["body"]["user_id"]
        title = todo_object["body"]["title"]
        current_timestamp = datetime.now()
        due_on = current_timestamp.isoformat()
        body_request_update = {
            "user_id": f"{usr_id}",
            "title": f"{title} Updated",
            "due_on": f"{due_on}",
            "status": "completed"
        }
        response = self.rest_client.request("put", f"{self.url_gorest_todos}/{id_}", body=body_request_update)
        return response

    def delete_todo(self, todo_id):
        LOGGER.debug("Cleanup todo")
        url_delete_todo = f"{URL_GOREST}/todos/{todo_id}"
        response = self.rest_client.request("delete", url_delete_todo)
        if response["status_code"] == 204:
            LOGGER.info("Deleted todo Id : %s", todo_id)
        return response

    def get_all_todos(self):
        url_todos = f"{URL_GOREST}/todos"
        response = self.rest_client.request("get", url_todos)
        return response

    def get_todo(self, todo_id):
        url_todo = f"{URL_GOREST}/todos/{todo_id}"
        response = self.rest_client.request("get", url_todo)
        return response
