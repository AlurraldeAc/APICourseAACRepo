import logging
import random

from faker import Faker

from config.config import URL_GOREST
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Post:

    def __init__(self, rest_client=None):
        self.url_gorest_posts = f"{URL_GOREST}/posts"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_post(self, user_id):
        number = random.randint(0, 999)
        body_post = {
            "user_id": f"{user_id}",
            "title": f"Post test {number}",
            "body": f"New post body {number}"
        }
        response = self.rest_client.request("posts", self.url_gorest_posts, body=body_post)
        return response

    def update_post(self, post_object):
        id_ = post_object["body"]["id"]
        usr_id = post_object["body"]["user_id"]
        title = post_object["body"]["title"]
        body = post_object["body"]["body"]
        body_request_update = {
            "user_id": f"{usr_id}",
            "title": f"{title} Updated",
            "body": f"{body} Updated"
        }
        response = self.rest_client.request("put", f"{self.url_gorest_posts}/{id_}", body=body_request_update)
        return response

    def delete_post(self, post_id):
        LOGGER.debug("Cleanup post")
        url_delete_post = f"{URL_GOREST}/posts/{post_id}"
        response = self.rest_client.request("delete", url_delete_post)
        if response["status_code"] == 204:
            LOGGER.info("Deleted post Id : %s", post_id)
        return response

    def get_all_post(self):
        url_posts = f"{URL_GOREST}/posts"
        response = self.rest_client.request("get", url_posts)
        return response

    def get_post(self, post_id):
        url_post = f"{URL_GOREST}/posts/{post_id}"
        response = self.rest_client.request("get", url_post)
        return response

