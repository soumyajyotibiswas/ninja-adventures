import sqlite3
from typing import Tuple

DATABASE = "data.db"

class Connections():

    def __init__(self) -> None:
        self.database = DATABASE
    
    def start_connection(self)-> Tuple['sqlite3.Connection', 'sqlite3.Connection']:
        connection = sqlite3.connect(self.database,isolation_level=None)
        cursor = connection.cursor()
        return (connection,cursor)
    
    @staticmethod
    def commit_connection(obj) -> None:
        obj.commit()

    @staticmethod
    def stop_connection(obj) -> None:
        obj.close()
