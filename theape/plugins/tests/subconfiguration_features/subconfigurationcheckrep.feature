Feature: SubConfiguration check_rep method
 Scenario: User calls check_rep on valid configuration
  Given SubConfiguration implementation with valid configuration
  When check_rep is called
  Then nothing happens

 Scenario: User calls check_rep on bad configuration
  Given SubConfiguration implementation with configuration errors
  When check_rep is checked
  Then a ConfigurationError is raised

 Scenario: User calls check_rep on configuration with extra values
  Given SubConfiguration implementation with unknown values
  When check_rep is checked
  Then a ConfigurationError is raised

 Scenario: User calls check_rep on configuration with allowed extra values
  Given SubConfiguration implementation with allowed unknown values
  When check_rep is checked
  Then a ConfigurationError not raised
  And the extra values are in the configuration
