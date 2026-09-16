Feature: Sidebar navigation
  Scenario: Switch between sidebar sections
    Given I am on the Accutai login page
    When I enter username "anjan" and password "123456"
    And I access the shared ledger
    And I click the "Dashboard" sidebar item
    Then I should see the "Finance Overview Dashboard" section

    When I click the "Shared Ledger All Team" sidebar item
    Then I should see the "Shared Company Ledger" section

    When I click the "Company Budget" sidebar item
    Then I should see the "Company Budget" section

    When I click the "Analytics & Reports" sidebar item
    Then I should see the "Analytics & Reports" section

    When I click the "Calendar View" sidebar item
    Then I should see the "Calendar View" section
