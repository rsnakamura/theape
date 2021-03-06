APESECTION = "APE"
MODULES_SECTION = 'MODULES'
FILE_TIMESTAMP = "%Y_%m_%d_%I:%M:%S_%p"
VERSION = "2014.12.28"

SUBCOMMAND_GROUP = 'theape.subcommands'


# these imports mean users of the parts of the ape need to have all dependencies installed
# even if the part they use doesn't need it...
from infrastructure.baseclass import BaseClass, BaseThreadClass
from infrastructure.errors import ApeError, DontCatchError, ConfigurationError
from infrastructure.indexbuilder import create_toctree
from plugins.base_plugin import BasePlugin, SubConfiguration, BaseConfiguration
from components.component import Component

# color_constants
BLUE = "\033[34m"
RED  = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"

NEWLINE = '\n'
# constants for formatting output
RED_THING =  "{red}{{{{thing}}}}{reset} {{verb}}".format(red=RED, reset=RESET)
BOLD_THING = "{bold}{{thing}}{reset} {{{{value}}}}".format(bold=BOLD, reset=RESET)
BLUE_WARNING = "{blue}{{thing}}{reset}".format(blue=BLUE, reset=RESET)
CALLED_ON = "'{blue}{{attribute}}{reset}' attribute called on {red}{{thing}}{reset}".format(blue=BLUE,
                                                                                             red=RED,
                                                                                             reset=RESET)

CREATION = RED_THING.format(verb='Created')
ARGS = BOLD_THING.format(thing='Args:')
KWARGS = BOLD_THING.format(thing='Kwargs:')
CALLED = RED_THING.format(verb='Called')
NOT_IMPLEMENTED = RED_THING.format(verb='Not Implemented')
