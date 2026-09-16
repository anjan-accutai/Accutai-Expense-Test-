Feature: Recent shared transactions search
  Scenario: Search and filter the ledger by keyword
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I create a transaction with date "2026-09-16", category "Office Supplies", description "tc11-search", and amount "10"
    And I search for "anjan" in the recent shared transactions table
    Then I should only see transactions matching "anjan"

    When I filter the recent shared transactions by category "Office Supplies"
    Then I should only see transactions matching "Office Supplies"

    When I search for "tc11-search" in the recent shared transactions table
    Then I should only see transactions matching "tc11-search"
