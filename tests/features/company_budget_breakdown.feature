Feature: Company Budget management
  @regression
  Scenario: Review company budget utilization and category breakdown
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I click the "Company Budget" sidebar item
    Then the Company Budget page should show utilization and category breakdown