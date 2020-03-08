"""
"""
import abc

class Db(object):
    """
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *params):
        pass

    @abc.abstractmethod
    def connect(self, *params):
        """
        """
        pass
    
    @abc.abstractmethod
    def insert(self, *params):
        """
        """
        pass