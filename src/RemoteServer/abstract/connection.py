"""
"""
import abc

class Connection(object):
    """
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def connect(self, *params):
        """
        """
        pass
