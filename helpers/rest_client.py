import json
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
        :return: response initially, after modifying for Validation purposes, response is a dictionary
        """
        response_dict = {}
        """
        This is to store these three elements from the the response in a dictionary
        response["status_code"]
        response["headers"]
        response["body"]
        """
        try:
            response = self.select_method(method_name, self.session)(url=url, data=body)
            LOGGER.debug("Response to request: %s", response.text)
            LOGGER.debug("Status Code: %s", response.status_code)
            # raise_for_status method from response to avoid the program crashes when error occurs.
            response.raise_for_status()
            if hasattr(response, "headers"):
                LOGGER.debug("Response Headers: %s", response.headers)
                response_dict["headers"] = response.headers
        # if HTTP error occurs
        except requests.exceptions.HTTPError as http_error:
            LOGGER.error("HTTP Error: %s", http_error)
            response_dict["headers"] = response.headers
        # if Request error occurs
        except requests.exceptions.RequestException as request_error:
            LOGGER.error("HTTP Error: %s", request_error)
        finally:
            if response.text:
                if response.ok:
                    response_dict["body"] = json.loads(response.text)
                else:
                    response_dict["body"] = {"msg": f"{response.text}"}
            else:
                response_dict["body"] = {"msg": "No body Content"}
        response_dict["status_code"] = response.status_code
        # return response
        return response_dict

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
            "posts": session.post,
            "put": session.put,
            "delete": session.delete
        }
        return methods.get(method_name)
