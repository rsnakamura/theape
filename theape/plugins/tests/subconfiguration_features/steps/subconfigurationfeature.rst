SubConfiguration
=================

.. literalinclude:: ../baseconfiguration.feature
   :language: gherkin




Scenario: User instantiates the SubConfiguration
-------------------------------------------------


.. code:: python

    @given("a SubConfiguration definition")
    def base_configuration_definition(context):
        context.definition = SubConfiguration
        return




.. code:: python

    @when("the user instantiates the SubConfiguration")
    def base_configuration_instantiation(context):
        context.callable = lambda : context.definition()
        return




.. code:: python

    @then("it raises a TypeError")
    def assert_raises(context):
        assert_that(calling(context.callable),
                    raises(TypeError))
        return



Scenario: User instantiates SubConfiguration implementation
------------------------------------------------------------


.. code:: python

    configspec = """
    plugin = option(Fake)
    
    op = string
    op2 = integer
    """.splitlines()
    
    class FakeConfiguration(SubConfiguration):
        def __init__(self, *args, **kwargs):
            super(FakeConfiguration, self).__init__(*args, **kwargs)
            return
    
        @property
        def product(self):
            return
    
        @property
        def configspec_source(self):
            if self._configspec_source is None:
                self._configspec_source = configspec
            return self._configspec_source
    
    config = """
    [FAKE]
    op = value
    """.splitlines()




.. code:: python

    @given("a SubConfiguration implementation")
    def base_configuration_implementation(context):
        context.configuration = ConfigObj(config)
        context.implementation = FakeConfiguration
        context.configspec_source = configspec
        context.section_name = 'FAKE'
        return




.. code:: python

    @when("the user instantiates the SubConfiguration implementation")
    def base_configuration_implementation_instantiation(context):
        context.configuration = context.implementation(source=context.configuration,
                                                       section_name=context.section_name,
                                                       configspec_source=context.configspec_source)
        return




.. code:: python

    @then("it has the SubConfiguration default properties")
    def assert_default_properties(context):
        assert_that(context.configuration.configuration,
                    is_(instance_of(ConfigObj)))
    
        assert_that(context.configuration.configspec,
                    is_(instance_of(ConfigObj)))
    
        assert_that(context.configuration.validator,
                    is_(instance_of(Validator)))
        return



Scenario: Configuration passes
------------------------------


.. code:: python

    valid_config_string = """
    [GOODBUTFAKE]
    plugin = Fake
    
    op = some value
    op2 = 75
    """.splitlines()
    
    @given("a SubConfiguration implementation with valid configuration")
    def valid_configuration(context):
        context.configuration = FakeConfiguration(source=ConfigObj(valid_config_string),
                                                  section_name='GOODBUTFAKE')
        return



When the SubConfiguration implementation processes the errors


.. code:: python

    @then("the process_errors outcome was False")
    def process_errors_false(context):
        assert_that(context.outcome,
                    is_(False))
        return



Scenario: Option fails validation
---------------------------------


.. code:: python

    bad_option_config = """
    [FAKE]
    plugin = Fake
    
    op = value
    op2 = not_integer
    """.splitlines()
    
    @given("a SubConfiguration implementation with a bad option")
    def bad_option(context):
        error = MagicMock()
        context.logger = MagicMock()
        context.logger.error = error
        bad_option_message = SubConfigurationConstants.bad_option_message
        context.expected = RED_ERROR.format(error='ConfigurationError',
                                            message=bad_option_message.format(option='op2',
                                                                              section='FAKE',
                                                                              error='the value "not_integer" is of the wrong type.',
                                                                              option_type='integer'))    
        context.configuration = FakeConfiguration(source=ConfigObj(bad_option_config),
                                                  section_name='FAKE')
        context.configuration._logger = context.logger
        return




.. code:: python

    @when("the SubConfiguration implementation processes the errors")
    def process_errors(context):
        outcome = context.configuration.configuration.validate(context.configuration.validator,
                                                               preserve_errors=True)
        context.outcome = context.configuration.process_errors()
        return




.. code:: python

    @then("the correct error message is logged")
    def check_error_message(context):
        context.logger.error.assert_called_with(context.expected)
        return




.. code:: python

    @then("the process_errors outcome was True")
    def process_errors_true(context):
        assert_that(context.outcome,
                    is_(True))
        return



Scenario: Missing Option
------------------------


.. code:: python

    missing_option_config = """
    [FAKE]
    plugin = Fake
    
    op = value
    """.splitlines()
    
    @given("a SubConfiguration implementation with a missing option")
    def missing_option(context):
        error = MagicMock()
        context.logger = MagicMock()
        context.logger.error = error
        missing_option_message = SubConfigurationConstants.missing_option_message
        context.expected = RED_ERROR.format(error='ConfigurationError',
                                            message=missing_option_message.format(option='op2',
                                                                                section='FAKE',
                                                                                plugin='Fake',
                                                                                option_type='integer'))    
        context.configuration = FakeConfiguration(source=ConfigObj(missing_option_config),
                                                  section_name='FAKE')
        context.configuration._logger = context.logger
    
        return



When the SubConfiguration implementation processes the errors, 
   Then the correct error message is logged

Scenario: Missing Section
-------------------------

Because the operators are expecting arbitrary section-names this last errors will only occur if the plugin has defined sub-section names in the configspec (I think).


.. code:: python

    # so the configspect can't have the top-level section name
    subsection_configspec = """
    plugin = string
    
    [sub_section]
    op1 = integer
    """.splitlines()
    
    missing_section_config = """
    [FAKE]
    plugin = fake_plugin
    """.splitlines()
    
    @given("a SubConfiguration implementation missing the section")
    def missing_section(context):
        error = MagicMock()
        context.logger = MagicMock()
        context.logger.error = error
        missing_section_message = SubConfigurationConstants.missing_section_message
        context.expected = RED_ERROR.format(error='ConfigurationError',
                                            message=missing_section_message.format(section='FAKE,sub_section',
                                                                                error='missing section',
                                                                                plugin='fake_plugin'))
        context.configuration = FakeConfiguration(source=ConfigObj(missing_section_config),
                                                  configspec_source=subsection_configspec,
                                                  section_name='FAKE')
        context.configuration._logger = context.logger
        return



When the SubConfiguration implementation processes the errors, 
   Then the correct error message is logged


Scenario: ConfigSpec Section Name Format
----------------------------------------


.. code:: python

    section_name_configspec = """
    op1 = integer
    
    [sub_section]
    op2 = integer
    """
    
    section_name_config = """
    [FAKE]
    op1 = 1
    
    [[sub_section]]
    op2 = 1
    """.splitlines()
    
    @given("a SubConfiguration configspec with section_name")
    def configspec_section_name(context):
        context.configuration = FakeConfiguration(source=ConfigObj(section_name_config),
                                                  configspec_source=section_name_configspec,
                                                  section_name='FAKE')
        context.configuration._logger = MagicMock()
        return




.. code:: python

    @when("the SubConfiguration implementation is checked")
    def check_implementation(context):
        context.configuration.process_errors()
        return




.. code:: python

    @then("the configuration outcome is True")
    def assert_outcome_true(context):
        assert_that(context.configuration.validation_outcome,
                    is_(True))
        return



Scenario: ConfigSpec string only has sub-section definition
-----------------------------------------------------------


.. code:: python

    subsection_only_configspec = """
    op1 = integer
    
    [sub_section]
    op2 = integer
    """
    @given("a SubConfiguration configspec without top-section")
    def configspec_subsection(context):
        context.configuration = FakeConfiguration(source=ConfigObj(section_name_config),
                                                  configspec_source=section_name_configspec,
                                                  section_name='FAKE')
        context.configuration._logger = MagicMock()
    
        return


   when the SubConfiguration implementation is checked
   Then the configuration outcome is True

Scenario: Configuration has extra values
----------------------------------------


.. code:: python

    extra_options_config = """
    [FAKE]
    op1 = 1
    
    [[sub_section]]
    op2 = 5
    op7 = 0
    
    [FAKE2]
    op1 = 3
    
    [[sub_section]]
    op2 = 4
    """.splitlines()
    
    @given("a SubConfiguration config with options not in the configspec")
    def extra_options(context):    
        context.logger = MagicMock()
        context.logger.warning = MagicMock()
        context.configuration = FakeConfiguration(source=ConfigObj(extra_options_config),
                                                  configspec_source=section_name_configspec,
                                                  section_name='FAKE')
        context.configuration._logger = context.logger
        return




.. code:: python

    @when("the SubConfiguration implementation checks extra values")
    def check_extra_values(context):
        context.outcome = context.configuration.check_extra_values()
        return




.. code:: python

    @then("the extra values are logged")
    def extra_values_logged(context):
        section = 'FAKE,sub_section'
        item_type = 'option'
        name = 'op7'
        message = SubConfigurationConstants.extra_message.format(section=section,
                                                                  item_type=item_type,
                                                                  name=name) + "='0'"
        context.logger.warning.assert_called_with(message)
        return




.. code:: python

    @then('check_extra_value returns True')
    def assert_extra_values(context):
        assert_that(context.outcome,
                    is_(True))
        return



Scenario: Configuration has no extra values
-------------------------------------------


.. code:: python

    no_extra_options_config = """
    [FAKE]
    op1 = 1
    
    [[sub_section]]
    op2 = 5
    """.splitlines()
    
    @given("a SubConfiguration config with no options not in the configspec")
    def no_extra_options(context):
        context.logger = MagicMock()
        context.logger.warning = MagicMock()
        context.configuration = FakeConfiguration(source=ConfigObj(no_extra_options_config),
                                                  configspec_source=section_name_configspec,
                                                  section_name='FAKE')
        context.configuration._logger = context.logger
    
        return



  When the SubConfiguration implementation checks extra values


.. code:: python

    @then("no extra values are logged")
    def no_logging(context):
        assert_that(context.logger.warning.mock_calls,
                    is_(equal_to([])))
        return




.. code:: python

    @then('check_extra_value returns False')
    def check_extra_false(context):
        assert_that(context.outcome,
                    is_(False))
        return



Scenario: Section updates configuration
---------------------------------------


.. code:: python

    update_sections_configspec = """
    updates_section = string(default=None)
    op1 = integer
    
    [sub_section]
    op2 = integer
    """
    
    update_sections_config = """
    [FAKE]
    op1 = 1
    
    [[sub_section]]
    op2 = 5
    
    [FAKE2]
    updates_section = FAKE
    
    [[sub_section]]
    op2 = 2
    """.splitlines()
    
    @given("a SubConfiguration section that updates another section")
    def updates_section(context):
        context.logger = MagicMock()
        context.logger.warning = MagicMock()
        context.fake1 = FakeConfiguration(source=ConfigObj(update_sections_config),
                                                  configspec_source=update_sections_configspec,
                                                  section_name='FAKE')
        context.fake2 = FakeConfiguration(source=ConfigObj(update_sections_config),
                                                  configspec_source=update_sections_configspec,
                                                  section_name='FAKE2')
        context.fake1._logger = context.logger
        context.fake2._logger = context.logger
        return




.. code:: python

    @when("the SubConfiguration implementation validates the configuration")
    def validate_configuration(context):
        return




.. code:: python

    @then("the SubConfiguration implementation will have the updates")
    def check_updates(context):
        #import pudb; pudb.set_trace()
        expected_fake = {'op1':1,
                         'sub_section': {'op2':5}}
        assert_that(context.fake1.configuration,
                    has_entries(expected_fake))
    
        expected_fake2 = {'op1':1,
                         'sub_section': {'op2':2}}
        assert_that(context.fake2.configuration,
                    has_entries(expected_fake2))
    
        return



Scenario: Configuration missing plugin name
-------------------------------------------


.. code:: python

    missing_plugin_name_config = """
    [FAKE]
    op = some string
    op2 = 42
    """.splitlines()
    
    @given("a SubConfiguration section missing a required plugin name")
    def missing_plugin_name(context):
        context.configuration = FakeConfiguration(source=ConfigObj(missing_plugin_name_config),
                                                  section_name='FAKE')
        return




.. code:: python

    @when("the SubConfiguration checks process_errors")
    def check_process_errors(context):
        context.callable = context.configuration.process_errors
        return




.. code:: python

    @then("the process_errors returned True")
    def process_errors_true(context):
        assert_that(calling(context.callable),
                    raises(ConfigurationError))
        return





.. code:: python

    @then("the configuration options that were given are in the configuration")
    def assert_options(context):
        expected = {'op':'some string',
                    'op2': 42}
        assert_that(context.configuration.configuration,
                    has_entries(expected))
        return


