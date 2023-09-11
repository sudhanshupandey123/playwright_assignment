Feature: Google Map

  Scenario Outline: Google Map Search with multiple values
    Given He Open Google Map
    When He Search For "<user_searched_for>"
    Then He Extract Information of Top "<user_requirement_value>" showing results
    And He Make CSV File Of Those
    Examples:
      | user_searched_for            | user_requirement_value |
      | resort near electronic city  | 15                     |
      | restaurant near marathahalli | 30                     |