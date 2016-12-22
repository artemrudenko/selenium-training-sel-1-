Scenario: Customer registration
    Given a customer list
    Given a valid customer
    When I register the customer
    Then new customer list contains all elements of the old customer list and a new element
