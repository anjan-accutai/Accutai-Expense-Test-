Feature: User profile and secure sign out
  Scenario: Verify profile details and sign out
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    Then I should see the correct user profile details
    When I click the Sign Out button
    Then I should be returned to the login page