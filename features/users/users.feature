@users @gorest @sanity
Feature: Users

  # Title of test case
  @normal
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA123
  @acceptance
  Scenario: Verify that Get all users endpoint returns all the existent users
    As I user, I want to get all users from GoRest API

    When I call the "users" endpoint using "GET" option
    Then I receive the response and validate with "Get_all_users" file
    And I validate the status code is 200


  @critical
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA123
  @acceptance @user_id
  Scenario: Verify that Get user endpoint returns a user by id
    As I user, I want to get a specific user from GoRest API

    When I call the Get "users" endpoint option with parameters
    Then I receive the response and validate with "Get_user" file
    And I validate the status code is 200


  @critical
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA123
  @acceptance
  Scenario: Verify that create user endpoint returns a created user
    As I user, I want to create a user in GoRest API

    When I call the "users" endpoint using "POST" option
    Then I receive the response and validate with "Create_user" file
    And I validate the status code is 201


  @trivial
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA123
  @acceptance @user_id
  Scenario: Verify that put user endpoint updates a created user
    As I user, I want to update a user from GoRest API

    When I call the "users" endpoint using "PUT" option
    Then I receive the response and validate with "Update_user" file
    And I validate the status code is 200


  @normal
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA123
  @acceptance @user_id
  Scenario: Verify that delete user endpoint deletes a user
    As I user, I want to delete a user from GoRest API

    When I call the "users" endpoint using "DELETE" option and with parameters
    Then I receive the response and validate with "Delete_user" file
    And I validate the status code is 204