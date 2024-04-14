import logging
import random

from faker import Faker

from config.config import URL_GOREST
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class User:

    def __init__(self, rest_client=None):
        self.url_gorest_users = f"{URL_GOREST}/users"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_user(self, body=None):
        body_user = body
        if body is None:
            number = random.randint(0,999)
            fake = Faker()
            name = fake.name()
            mail = name.lower().replace(" ", "")
            body_user = {
                "name": f"{name}",
                "email": f"{mail}_{number}@mail.com",
                "gender": "male",
                "status": "active"
            }
        response = self.rest_client.request("posts", self.url_gorest_users, body=body_user)

        return response, self.rest_client

    def update_user(self, user):
        id_ = user["body"]["id"]
        name = user["body"]["name"]
        email = user["body"]["email"]
        body_request_update = {
            "name": f"{name}",
            "email": f"{email}",
            "gender": "female",
            "status": "inactive"
        }
        response = self.rest_client.request("put", f"{self.url_gorest_users}/{id_}", body=body_request_update)

        return response

    def delete_user(self, user_id):
        LOGGER.debug("Cleanup user")
        url_delete_user = f"{URL_GOREST}/users/{user_id}"
        response = self.rest_client.request("delete", url_delete_user)
        if response["status_code"] == 204:
            LOGGER.info("Deleted user Id : %s", user_id)
        return response

    def get_all_users(self):
        url_users = f"{URL_GOREST}/users/"
        response = self.rest_client.request("get", url_users)
        return response

    def get_user(self, user_id):
        url_user = f"{URL_GOREST}/users/{user_id}"
        response = self.rest_client.request("get", url_user)
        return response

    def create_missing_name(self):
        body_user = {
            "name": "",
            "email": "username@mail.com",
            "gender": "male",
            "status": "active"
            }
        response = self.rest_client.request("posts", self.url_gorest_users, body=body_user)
        return response

    def already_taken_email(self, user_object):
        email = user_object["body"]["email"]
        body_user = {
            "name": "New username",
            "email": f"{email}",
            "gender": "male",
            "status": "active"
            }
        response = self.rest_client.request("posts", self.url_gorest_users, body=body_user)
        return response


