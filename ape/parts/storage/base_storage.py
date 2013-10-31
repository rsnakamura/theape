
# python standard library
from abc import ABCMeta, abstractproperty, abstractmethod

# this package
from ape import BaseClass
from ape import ApeError


class BaseStorage(BaseClass):
    """A base-class based on file-objects"""
    def __init__(self):
        """
        BaseStorage Constructor
        """
        __metaclass__ = ABCMeta
        super(BaseStorage, self).__init__()
        self._logger = None
        self.closed = True
        self._file = None
        return

    @abstractproperty
    def file(self):
        """
        The open file object
        """
    
    def close(self):
        """
        Closes self.file
        """
        self.file.close()
        self.closed = True
        return
    
    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__,
                                 self.name)


    @abstractmethod
    def open(self, name):
        """
        Opens a file for writing

        :param:

         - `name`: a basename (no path) for the file

        :return: copy of self with file as open file and closed set to False
        """
        return 

    @abstractmethod
    def close(self):
        """
        Closes self.file if it exists, sets self.closed to True
        """
        return

    def write(self, text):
        """
        Writes the text to the file        
        """
        try:
            self.file.write(text)
        except (AttributeError, ValueError) as error:
            self.logger.debug(error)
            error = "{red}{bold}`write` called on unopened file{reset}"
            raise ApeError(error)
        return

    def writeline(self, text):
        """
        Adds newline to end of text and writes it to the file
        """
        self.write("{0}\n".format(text))
        return

    def writelines(self, texts):
        """
        Writes the lines to the file

        :param:

         - `texts`: collection of strings
        """
        try:
            self.file.writelines(texts)
        except (AttributeError, ValueError) as error:
            self.logger.debug(error)
            error = "{red}{bold}`write` called of unopened file{reset}"
            raise ApeError(error)
        return        
# end BaseStorage    
