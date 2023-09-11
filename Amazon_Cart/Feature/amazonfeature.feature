Feature: Amazon Cart

  Scenario: Amazon Cart Review
    Given User is on Amazon Page
    When He Search For Product "Dell Laptop" and filtering based on rating "4"
    And He add first "2" product to cart
    Then the cart value should be sum of products

  Scenario Outline: : Amazon Cart Review
    Given User is on Amazon Page
    When He Search For Product "<product>" and filtering based on rating "<rating>"
    And He add first "<product_count>" product to cart
    Then the cart value should be sum of products
    Examples:
      | product       | rating | product_count |
      | Lenovo Laptop | 3      | 1             |

