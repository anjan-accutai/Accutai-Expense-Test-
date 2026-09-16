Feature: Shared Company Ledger audit view
  Scenario: Review shared transaction audit data
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I click the "Shared Ledger All Team" sidebar item
    Then the Shared Ledger should show transaction audit columns and filters