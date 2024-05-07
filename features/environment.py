import logging

from config.config import URL_GOREST
from entities.todo import Todo
from entities.user import User
from entities.post import Post

from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    """
    Fixture to initialize variables and objects
    :param context:
    """
    LOGGER.info("Before all")
    # context.url = URL_GOREST
    # LOGGER.info(type(context))
    # if hasattr(context, "url"):
    #     LOGGER.info("URL: %s", context.url)
    context.rest_client = RestClient()
    context.url_gorest_users = f"{URL_GOREST}/users"
    context.url_gorest_posts = f"{URL_GOREST}/posts"
    context.url_gorest_todos = f"{URL_GOREST}/todos"
    # response = context.rest_client.request("get", context.url_gorest_users)
    # context.user_id = response["body"][0]["id"]
    # LOGGER.debug("User Id: %s", context.user_id)
    # context.user_created_list = []
    context.resource_list = {
        "todos": [],
        "posts": [],
        "users": []
    }
    context.validate = ValidateResponse()
    context.user = User()
    context.postOb = Post()
    context.todo = Todo()


def before_feature(context, feature):
    """

    :param context:
    :param feature:
    """
    LOGGER.info("Before feature")


def before_scenario(context, scenario):
    """

    :param context:
    :param scenario:
    """
    context.resource_list = {
        "todos": [],
        "posts": [],
        "users": []
    }
    LOGGER.info("\n***** - Before Scenario - *****")
    LOGGER.info("Test '%s' STARTED \n", scenario.name)

    if "user_id" in scenario.tags:
        new_user = context.user.create_user()
        context.user_id = new_user["body"]["id"]
        context.resource_list["users"].append(context.user_id)
        LOGGER.warning(context.resource_list)

    if "post_id" in scenario.tags:
        user_id = context.user_id
        new_post = context.postOb.create_post(user_id)
        context.post_id = new_post["body"]["id"]
        context.resource_list["posts"].append(context.post_id)
        LOGGER.warning(context.resource_list)

    if "todo_id" in scenario.tags:
        user_id = context.user_id
        new_todo = context.todo.create_todo(user_id)
        context.todo_id = new_todo["body"]["id"]
        context.resource_list["todos"].append(context.todo_id)
        LOGGER.warning(context.resource_list)


def after_scenario(context, scenario):
    """

    :param context:
    :param scenario:
    """
    LOGGER.info("\n***** After scenario *****")
    for resource in context.resource_list:
        for resource_id in context.resource_list[resource]:
            url_delete_project = f"{URL_GOREST}/{resource}/{resource_id}"
            LOGGER.info("%s Id to be deleted : %s", resource, resource_id)
            response = context.rest_client.request("delete", url_delete_project)
            if response["status_code"] == 204:
                LOGGER.info("%s Id deleted : %s", resource, resource_id)
                LOGGER.warning("State List after Scenario: %s", context.resource_list)


def after_feature(context, feature):
    """

    :param context:
    :param feature:
    """
    LOGGER.info("After feature")


def after_all(context):
    """

    :param context:
    """
    LOGGER.info("After all")