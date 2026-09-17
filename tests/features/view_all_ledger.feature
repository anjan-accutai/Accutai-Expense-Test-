Feature: View All in Ledger shortcut
  @regression
  Scenario: Open the full Shared Ledger from the dashboard
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I click the View All in Ledger shortcut
    Then I should be on the full Shared Ledger view