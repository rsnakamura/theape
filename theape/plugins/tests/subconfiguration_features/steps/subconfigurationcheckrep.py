
#third-party
from behave import given, when, then
from hamcrest import assert_that, is_, calling, raises, equal_to
from configobj import ConfigObj

# this package
from theape.plugins.base_plugin import SubConfiguration, ConfigurationError

configspec_source = """
plugin = option('Concrete')

op1 = integer
op2 = integer
"""

class ConcreteConfiguration(SubConfiguration):
    """
    Test configuration
    """
    
    @property
    def configspec_source(self):
        if self._configspec_source is None:
            self._configspec_source = configspec_source
        return self._configspec_source

    @property
    def product(self):
        return

valid_configuration = """
[cement]
plugin = Concrete
op1 = 53
op2 = 64
""".splitlines()

@given("SubConfiguration implementation with valid configuration")
def step_implementation(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(valid_configuration),
                                                  section_name='cement')
    return

@when("check_rep is called")
def step_implementation(context):
    context.outcome = context.configuration.check_rep()
    return

@then("nothing happens")
def step_implementation(context):
    assert_that(context.outcome,
                is_(None))
    return

invalid_configuration = """
[konkrete]
plugin = Concrete
op1 = apple
op2 = banana
""".splitlines()

@given("SubConfiguration implementation with configuration errors")
def step_implementation(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(invalid_configuration),
                                                  section_name='konkrete')
        
    return

@when("check_rep is checked")
def check_rep_check(context):
    context.callable = context.configuration.check_rep
    return

@then("a ConfigurationError is raised")
def step_implementation(context):
    assert_that(calling(context.callable),
                raises(ConfigurationError))
    return

extra_option_configuration = """
[cement]
plugin = Concrete
op1 = 53
op2 = 64
ummagumma = apple_banana
""".splitlines()

@given("SubConfiguration implementation with unknown values")
def step_implementation(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(extra_option_configuration),
                                                  section_name='cement')
    return

@given("SubConfiguration implementation with allowed unknown values")
def allowed_unknowns(context):
    context.configuration = ConcreteConfiguration(source=ConfigObj(extra_option_configuration),
                                                  section_name='cement',
                                                  allow_extras=True)
    return

@then("a ConfigurationError not raised")
def no_error(context):
    context.callable()
    return

@then("the extra values are in the configuration")
def assert_extras(context):
    assert_that(context.configuration.configuration['ummagumma'],
                is_(equal_to('apple_banana')))