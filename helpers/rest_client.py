import logging

import requests

from config.config import HEADERS_GOREST
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:

    def __init__(self, headers=HEADERS_GOREST):
        self.session = requests.Session()
        self.session.headers.update(headers)

    def request(self, method_name, url, body=None):
        """

        :param method_name:
        :param url:
        :param body:
        :return:
        """
        response = self.select_method(method_name, self.session)(url=url, data=body)
        if response.text:
            LOGGER.debug("Response to request(json): %s", response.json())
        else:
            LOGGER.debug("Response to request(text): %s", response.text)
        LOGGER.debug("Status Code: %s", response.status_code)
        return response

    @staticmethod
    def select_method(method_name, session):
        """
        Select REST method with session object
        :param method_name:
        :param session:
        :return:
        """
        methods = {
            "get": session.get,
            "post": session.post,
            "put": session.put,
            "delete": session.delete
        }
        return methods.get(method_name)
