@taskledger:TL-0042
Feature: Password login

  @ac:AC-001
  Scenario: Reject invalid password
    Given a registered user exists
    When the user submits an invalid password
    Then login is rejected
    And no authenticated session is created
