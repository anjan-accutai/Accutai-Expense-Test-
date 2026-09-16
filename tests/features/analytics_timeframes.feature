Feature: Analytics timeframe toggles
  Scenario: Switch between monthly quarterly and yearly analytics
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I click the "Analytics & Reports" sidebar item
    And I switch through the analytics timeframes
    Then the analytics period overview should update