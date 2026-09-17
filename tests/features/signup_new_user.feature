Feature: New user registration
  @regression
  Scenario: Create a new user account
    Given I am on the Accutai login page
    When I click Register
    And I enter a new username and email and password
    Then I should see the authenticating state
