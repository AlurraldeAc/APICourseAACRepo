import json
import logging
import random

from faker import Faker

from utils.logger import get_logger
from behave import when, then

LOGGER = get_logger(__name__, logging.DEBUG)


# Get
@when(u'I call the "{endpoint}" endpoint using "GET" option')
def call_endpoint(context, endpoint):
    LOGGER.debug(f"STEP: When I call the '{endpoint}' endpoint using 'GET' option")
    url_endpoint = get_url_by_feature(context, endpoint)
    response = context.rest_client.request("get", url_endpoint)
    context.response = response
    context.endpoint = endpoint


@when(u'I call the {method_name} "{endpoint}" endpoint option with parameters')
def call_endpoint(context, method_name, endpoint):
    LOGGER.info(f"STEP: When I call {method_name} '{endpoint}' endpoint option with parameters")
    LOGGER.info("Test GET by Id")
    url_endpoint = get_url_by_feature(context, endpoint, resource_id=True)
    response = context.rest_client.request("get", url_endpoint)
    context.response = response
    context.endpoint = endpoint


# Delete
@when(u'I call the "{endpoint}" endpoint using "DELETE" option and with parameters')
def step_impl(context, endpoint):
    LOGGER.info(f'STEP: I call the "{endpoint}" endpoint using "DELETE" option and with parameters')
    url_delete = get_url_by_feature(context, endpoint, resource_id=True)
    response = context.rest_client.request("delete", url_delete)
    context.response = response
    context.endpoint = endpoint
    context.resource_list[endpoint].pop()
    LOGGER.warning("List after deleting: %s", context.resource_list)


# Post / Put
@when(u'I call the "{endpoint}" endpoint using "{method}" option')
def call_endpoint(context, endpoint, method):
    LOGGER.info(f'STEP: when I call the "{endpoint}" endpoint using "{method}" option')
    # url depends on @user_id tag and attribute user_id
    resource_id = False
    if method.lower() == 'put':
        resource_id = True
    url_endpoint = get_url_by_feature(context, endpoint, resource_id)

    if context.text:
        LOGGER.debug("JSON Doc string: %s", context.text)
        body_endpoint = update_json_doc_string_param(context, json.loads(context.text))
    else:
        number = random.randint(0, 999)
        fake = Faker()
        name = fake.name()
        mail = name.lower().replace(" ", "")
        body_endpoint = {
            "name": f"{name}",
            "email": f"{mail}_{number}@mail.com",
            "gender": "male",
            "status": "active"
        }
    # call rest_client by method (method name to lowercase)
    response = context.rest_client.request(method.lower(), url_endpoint, body=body_endpoint)
    if method.lower() == 'post':
        # add to list of resources the resource created (id)
        resource_id = response["body"]["id"]
        context.resource_list[endpoint].append(resource_id)
    # store in context response and endpoint
    context.response = response
    context.endpoint = endpoint


@then(u'I receive the response and validate with "{json_file}" file')
def receive_response(context,  json_file):
    LOGGER.info(f"STEP: I receive the response and validate with {json_file} file")
    context.validate.validate_response(context.response, context.endpoint, json_file)


@then(u'I validate the status code is {status_code:d}')
def validate_status_code(context, status_code):
    LOGGER.info(f"STEP: Then I validate the status code is {status_code}")
    assert context.response["status_code"] == status_code, \
        f"Expected {status_code} but received {context.response['status_code']}"


def get_url_by_feature(context, endpoint, resource_id=False):
    url = None
    if endpoint == "users":
        if resource_id:
            if hasattr(context, "user_id"):
                url = context.url_gorest_users + "/" + str(context.user_id)
        else:
            url = context.url_gorest_users
    elif endpoint == "posts":
        if resource_id:
            if hasattr(context, "post_id"):
                url = context.url_gorest_posts + "/" + str(context.post_id)
        else:
            url = context.url_gorest_posts
    elif endpoint == "todos":
        if resource_id:
            if hasattr(context, "todo_id"):
                url = context.url_gorest_todos + "/" + str(context.todo_id)
        else:
            url = context.url_gorest_todos

    return url


def update_json_doc_string_param(context, json_doc_string_data):
    keys = ["user_id", "post_id", "todo_id"]
    for id_type in keys:
        for id_in_doc_string in json_doc_string_data.keys():
            if id_in_doc_string == id_type and hasattr(context, id_type):
                json_doc_string_data[id_in_doc_string] = getattr(context, id_type)  # e.g. "user_id" = "548882893"
                LOGGER.debug("Key changed %s: ", id_in_doc_string)
    LOGGER.debug("New JSON data: %s", json_doc_string_data)

    return json_doc_string_data
