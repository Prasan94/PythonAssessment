"""
"""
from pymongo import MongoClient
from src.DB.abstract.db import Db as absDb

class MongoDB(absDb):
    """
    """
    def __init__(self, uri, dataBase):
        self.connection = MongoClient(uri)
        self.db = conn.database #replace with actual db
        self.collection = db.collection
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            print("Error Occurred in DB operation: %s"%exec_val)
        self.connection.close()

    def update(self, document):
        """
        """
        self.db.update({cell_id:document["cellId"]},{$set : document}, {upsert:true})
    
