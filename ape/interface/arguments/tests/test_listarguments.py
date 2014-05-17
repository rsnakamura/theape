
#python standard library
import unittest

# the ape
from ape.interface.arguments.listarguments import ListArguments


class TestListArguments(unittest.TestCase):
    def setUp(self):
        self.args = ['list']
        self.arguments = ListArguments(args=self.args)
        return
    
    def test_constructor(self):
        """
        Does it build correctly?
        """
        arguments = ListArguments(args=['list'])

        # inderited default
        self.assertFalse(arguments.pudb)
        return

    def test_modules(self):
        """
        Does it get the list of plugin modules?
        """
        # default to empty list
        self.assertEqual([], self.arguments.modules)

        # positional arguments
        modules = 'ape bat chameleon'.split()
        self.arguments.reset()
        self.arguments.args = self.args + modules
        self.assertEqual(modules, self.arguments.modules)
        return        
