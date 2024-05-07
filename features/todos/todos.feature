@todos @gorest @sanity
Feature: Todos

  # Title of test case
  @critical
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA456
  @acceptance
  Scenario: Verify that Get all Todos endpoint returns all the existent todo objects
    As I user, I want to get all todo objects from the GoRest API

    When I call the "todos" endpoint using "GET" option
    Then I receive the response and validate with "Get_all_todos" file
    And I validate the status code is 200

  @normal
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA456
  @acceptance @user_id @todo_id
  Scenario: Verify that Get todos endpoint returns a "todo" object by id
    As I user, I want to get a specific "todo" object from the GoRest API

    When I call the Get "todos" endpoint option with parameters
    Then I receive the response and validate with "Get_todo" file
    And I validate the status code is 200

  @trivial
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA456
  @acceptance @user_id
  Scenario Outline: Verify that many objects can be created by the "todos" endpoint option POST
    As I user, I want to create many "todo" objects on the GoRest API

    When I call the "todos" endpoint using "POST" option
    """
      {
        "user_id": "user_id",
        "title": "Todo object test <errand_name>",
        "due_on": "<due_date>",
        "status": "pending"
      }
    """
    Then I receive the response and validate with "Create_todo" file
    And I validate the status code is 201

    Examples:
      | errand_name                   | due_date                 |
      | Complete build model one      | 2024-05-14T00:00:00.000  |
      | Complete review model two     | 2024-05-15T00:00:00.000  |
      | Complete build model three    | 2024-05-16T00:00:00.000  |
      | Complete project models four  | 2024-05-17T00:00:00.000  |
