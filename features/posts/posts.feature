@posts @gorest @sanity
Feature: Posts

  # Title of test case
  @trivial
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA321
  @acceptance
  Scenario: Verify that Get all Posts endpoint returns all the existent posts
    As I user, I want to get all posts published on GoRest API

    When I call the "posts" endpoint using "GET" option
    Then I receive the response and validate with "Get_all_posts" file
    And I validate the status code is 200


  @critical
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA321
  @acceptance @user_id @post_id
  Scenario: Verify that Get posts endpoint returns a "post" by id
    As I user, I want to get a specific "post" from GoRest API

    When I call the Get "posts" endpoint option with parameters
    Then I receive the response and validate with "Get_post" file
    And I validate the status code is 200


  @critical
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA321
  @acceptance @user_id
  Scenario Outline: Verify that many objects can be created by the "posts" endpoint option POST
    As I user, I want to create many "post" objects on the GoRest API

    When I call the "posts" endpoint using "POST" option
    """
      {
        "user_id": "userId",
        "title": "Post test <post_name>",
        "body": "New post body <body_msg>"
      }
    """
    Then I receive the response and validate with "Create_post" file
    And I validate the status code is 201

    Examples:
      | post_name             | body_msg                 |
      | New post name one     | Text on New post one     |
      | New post name two     | Text on New post two     |
      | New post name three   | Text on New post three   |
      | New post name four    | Text on New post four    |


  @trivial
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA321
  @acceptance @user_id @post_id
  Scenario: Verify that put Posts endpoint updates a created post object
    As I user, I want to update a post object from GoRest API

    When I call the "posts" endpoint using "PUT" option
    Then I receive the response and validate with "Update_post" file
    And I validate the status code is 200


  @normal
  @allure.label.owner:Ariel_Alurralde
  @allure.link:https://dev.example.com/
  @allure.issue:API-QA321
  @acceptance @user_id @post_id
  Scenario: Verify that delete posts endpoint deletes a post object
    As I user, I want to delete a post object from GoRest API

    When I call the "posts" endpoint using "DELETE" option and with parameters
    Then I receive the response and validate with "Delete_post" file
    And I validate the status code is 204
