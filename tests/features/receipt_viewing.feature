Feature: Receipt viewing
  Scenario: View an attached receipt from a transaction
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I create a transaction with an attached receipt
    Then I should be able to view the attached receipt