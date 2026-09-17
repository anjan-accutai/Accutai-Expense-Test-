Feature: Future expense planning
  @regression
  Scenario: Record a future dated expense
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I create a future transaction for "2026-10-16"
    Then the future transaction should be recorded