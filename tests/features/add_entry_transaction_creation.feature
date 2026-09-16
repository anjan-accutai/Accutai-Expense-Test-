Feature: Add entry transaction creation
  Scenario: Record a transaction for each category
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I add a transaction for every category with date "2026-09-11", description "test", and amount "10"
    Then I should see the new transaction for every category in the recent shared transactions table
