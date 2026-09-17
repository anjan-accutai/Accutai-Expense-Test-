Feature: Valid user login
  @smoke
  Scenario: Login with valid credentials
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    Then I should see the Finance Overview Dashboard
