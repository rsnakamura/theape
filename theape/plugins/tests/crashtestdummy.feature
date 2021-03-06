Feature: Crash Test Dummy
 Scenario: User doesn't specify any options
  Given an empty crash test dummy configuration
  When the configuration is checked
  Then the crash test dummy configuration has the defaults
  And it is a Base Configuration

 Scenario: User passes in wrong plugin
  Given a crash test dummy with the wrong plugin name
  When the configuration with the wrong plugin is checked
  Then the crash test dummy validator will raise a ConfigurationError

 Scenario: User gets CrashTestDummy
  Given a CrashTestDummy Configuration
  When the user gets the CrashTestDummy product
  Then the CrashTestDummy is correctly configured
