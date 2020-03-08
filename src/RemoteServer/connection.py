"""
"""
import pysftp
from src.RemoteServer.abstract.connection import Connection as absConnection
from src.utils.helper import SingleTon

class FtpConnection(absConnection, SingleTon):
    """
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.cnopts = None
        
    @property
    def cnopts(self, _):
        """
        """
        return self._cnopts

    @cnopts.setter
    def cnopts(self, _):
        """
        """
        try:
            self._cnopts = pysftp.CnOpts()
            self._cnopts.hostkeys = None
        except Exception as err:
            raise Exception("Error in setting host key: %s"%err)

    def connect(self):
        """
        """
        return pysftp.Connection(host=self.host, username=self.user, password=self.password, cnopts=self.cnopts)

