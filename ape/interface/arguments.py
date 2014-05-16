
"""APE (the all-purpose-evaluator)

Usage: ape -h | -v
       ape [--debug|--silent] [--pudb|--pdb] <command> [<argument>...]
       ape [--debug|--silent] [--trace|--callgraph] <command> [<argument>...]

Help Options:

    -h, --help     Display this help message and quit.
    -v, --version  Display the version number and quit.
    
Logging Options:

    --debug   Set logging level to DEBUG.
    --silent  Set logging level to ERROR.

Debugging Options:

    --pudb       Enable the `pudb` debugger (if installed)
    --pdb        Enable the `pdb` (python's default) debugger
    --trace      Enable code-tracing
    --callgraph  Create a call-graph of for the code

Positional Arguments:

    <command>      The name of a sub-command (see below)
    <argument>...  One or more options or arguments for the sub-command
    
Available Sub-Commands:

    run    Run a plugin
    fetch  Fetch a sample configuration-file
    help   Display more help
    list   List known plugins
    check  Check a configuration

"""     


# python standard library
import argparse

# third-party
import docopt

# this package
from ubootkommandant import UbootKommandant
from ape import BaseClass, VERSION


document_this = __name__ == '__builtin__'


class ArgumentClinic(object):
    """
    A command-line argument parser
    """
    def __init__(self):
        """
        The ArgumentClinic Constructor
        """
        self._subcommand = None
        self._parser = None        
        self._subparsers = None
        self._args = None
        self._subparser_list = None
        return

    @property
    def subparser_list(self):
        """
        This is here so that the Ape Plugin could have access to the sub-parser help

        :return: list of sub-parsers added to the main ArgumentParser
        """
        if self._subparser_list is None:
            self._subparser_list = []
        return self._subparser_list

    @property
    def subcommand(self):
        """
        The sub-command strategies for the sub-parsers
        """
        if self._subcommand is None:
            self._subcommand = UbootKommandant()
        return self._subcommand        

    @property
    def subparsers(self):
        """
        sub-parsers for the parser
        """
        if self._subparsers is None:
            self._subparsers = self.parser.add_subparsers(title='Sub-Commands Help',
                                                          description='Available Subcommands',
                                                          help="SubCommands")
        return self._subparsers

    @property
    def parser(self):
        """
        An ArgumentParser
        """
        if self._parser is None:
            self._parser = argparse.ArgumentParser(prog=__package__)            
        return self._parser

    def add_arguments(self):
        """
        Adds the arguments to the parser
        """
        self.parser.add_argument('--debug',
                                 help='Sets the logging level to debug',
                                 action='store_true',
                                 default=False)
        self.parser.add_argument('-v', '--version', help='Display the version number and quit',
                         action='version', version="%(prog)s {0}".format(VERSION))    

        self.parser.add_argument('--silent',
                                 help='Sets the logging level to off (for stdout)',
                                 action='store_true',
                                 default=False)
        self.parser.add_argument('--pudb',
                                  help='Enables the pudb debugger',
                                  action='store_true',
                                  default=False)
        self.parser.add_argument('--pdb',
                                help='Enables the pdb debugger',
                                action='store_true',
                                default=False)
        self.parser.add_argument('--trace',
                                 help='Turn on code-tracing',
                                 action='store_true',
                                 default=False)

        self.parser.add_argument('--callgraph',
                                 help='Create call-graph',
                                 action='store_true',
                                 default=False)
        return
    
    def add_subparsers(self):
        """
        Adds subparsers to the parser

        I am now adding these to self so that the sub-parsers are public

        :postcondition: self.subparser_list is a list of the added sub-parsers
        """
        # run sub-command
        self.runner = self.subparsers.add_parser("run",
                                                 help="Run the Ape")
        self.subparser_list.append(self.runner)
        self.runner.add_argument("configfiles",
                                 help="A list of config file name (default='%(default)s').",
                                 metavar="<config-file list>",
                                 default=["ape.ini"],
                                 nargs="*")
        self.runner.set_defaults(function=self.subcommand.run)

        # fetch sub-command
        self.fetcher = self.subparsers.add_parser("fetch",
                                                  help="Fetch a sample config file.")

        self.subparser_list.append(self.fetcher)
        self.fetcher.add_argument('names',
                                  help="List of plugin-names (default=%(default)s)",
                                  default=["Ape"],
                                  nargs="*")
        self.fetcher.add_argument('--modules',
                                help='Non-ape modules',
                                nargs='*')
        self.fetcher.set_defaults(function=self.subcommand.fetch)

        # list sub-command
        self.lister = self.subparsers.add_parser("list",
                                                 help="List available plugins.")
        self.subparser_list.append(self.lister)
        self.lister.add_argument('--modules',
                                 help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')
        self.lister.set_defaults(function=self.subcommand.list_plugins)

        # check sub-command
        self.checker = self.subparsers.add_parser('check',
                                                  help='Check your setup.')

        self.subparser_list.append(self.checker)
        self.checker.add_argument("configfiles",
                                  help="List of config files (e.g. *.ini - default='%(default)s').",
                                  metavar="<config-file list>",
                                  default=["ape.ini"],
                                  nargs="*")
        self.checker.add_argument("--modules",
                                  help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')

        self.checker.set_defaults(function=self.subcommand.check)

        # help sub-command
        self.helper = self.subparsers.add_parser("help",
                                                 help="Show more help")

        self.subparser_list.append(self.helper)
        self.helper.add_argument('name',
                                 help="A specific plugin to inquire about.",
                                 nargs="?", default='Ape')
        self.helper.add_argument('-w', '--width',
                                 help="Number of characters to wide to format the page.",
                                 type=int, default=70)
        self.helper.add_argument('--modules',
                                 help='Space-separated list of non-ape modules with plugins',
                                 nargs='*')

        self.helper.set_defaults(function=self.subcommand.handle_help)
        return
    
    @property
    def args(self):
        """
        The parsed args (adds arguments and sub-commands first)
        """
        if self._args is None:
            self.add_arguments()
            self.add_subparsers()
            self._args =  self.parser.parse_args()
        return self._args

    def __call__(self):
        """
        The main interface

        :return: argparse namespace
        """
        return self.args
# end class ArgumentClinic        


class ArgumentsConstants(object):
    """
    Constants for the arguments
    """
    __slots__ = ()
    debug = "--debug"
    silent = '--silent'
    pudb = "--pudb"
    pdb = '--pdb'
    trace = '--trace'
    callgraph = '--callgraph'
    command = "<command>"
    argument = '<argument>'
# end ArgumentConstants    


class BaseArguments(BaseClass):
    def __init__(self, usage=__doc__, args=None, options_first=True):
        """
        BaseArguments constructor

        :param:

         - `usage`: usage string for `docopt`
         - `args`: list of arguments for `docopt`
         - `options_first`: docopt parameter to grab all options (or not)
        """
        super(BaseArguments, self).__init__()
        self._logger = None
        self.options_first = options_first
        self.usage = usage
        self.args = args
        self._debug = None
        self._silent = None
        self._arguments = None
        self._pudb = None
        self._pdb = None
        self._trace = None
        self._callgraph = None
        return

    @property
    def arguments(self):
        """
        Dictionary of arguments
        """
        if self._arguments is None:
            self._arguments = docopt.docopt(doc=self.usage,
                                            argv=self.args,
                                            options_first=self.options_first,
                                            version=VERSION)
        return self._arguments

    @property
    def debug(self):
        """
        Option to change logging level to debug

        :rtype: Boolean
        """
        if self._debug is None:
            self._debug = self.arguments[ArgumentsConstants.debug]
        return self._debug

    @property
    def silent(self):
        """
        Option to change logging level to error
        :rtype: Boolean
        """
        if self._silent is None:
            self._silent = self.arguments[ArgumentsConstants.silent]
        return self._silent

    @property
    def pudb(self):
        """
        Option to enable pudb debugger
        :rtype: Boolean
        """
        if self._pudb is None:
            self._pudb = self.arguments[ArgumentsConstants.pudb]
        return self._pudb

    @property
    def pdb(self):
        """
        Option to enable the python debugger
        :rtype: Boolean
        """
        if self._pdb is None:
            self._pdb = self.arguments[ArgumentsConstants.pdb]
        return self._pdb

    @property
    def trace(self):
        """
        Option to turn on code tracing
        :rtype: Boolean
        """
        if self._trace is None:
            self._trace = self.arguments[ArgumentsConstants.trace]
        return self._trace

    @property
    def callgraph(self):
        """
        Option to create a callgraph
        :rtype: Boolean
        """
        if self._callgraph is None:
            self._callgraph = self.arguments[ArgumentsConstants.callgraph]
        return self._callgraph

    def reset(self):
        """
        resets the properties to None
        """
        self._callgraph = None
        self._trace = None
        self._arguments = None
        self._debug = None
        self._silent = None
        self._pudb = None
        self._pdb = None
        return
# end class BaseArguments    
