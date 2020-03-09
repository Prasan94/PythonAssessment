"""
"""
import abc

class Db(object):
    """
    """

    __metaclass__ = abc.ABCMeta
  
    @abc.abstractmethod
    def update(self, *params):
        """
        """
        pass
