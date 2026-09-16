Feature: Monthly budget metrics
  Scenario: View monthly budget and financial metrics
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    Then I should see the monthly budget and financial metrics
