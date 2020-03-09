"""
"""
from pymongo import MongoClient
from src.DB.abstract.db import Db as absDb

class MongoDB(absDb):
    """
    """
    def __init__(self, uri):
        self.connection = MongoClient(uri)
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.connection.close()

    def insert(self):
        """
        """
        pass
    
