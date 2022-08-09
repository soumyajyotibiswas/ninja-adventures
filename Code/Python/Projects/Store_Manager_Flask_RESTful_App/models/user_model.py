import sys,os
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}')
from connections import Connections

class UserModel:
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls,username):
        database_connections = Connections()
        connection, cursor = database_connections.start_connection()
        find_user = "SELECT * from users WHERE username=?"
        result = cursor.execute(find_user,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):
        database_connections = Connections()
        connection, cursor = database_connections.start_connection()
        find_user = "SELECT * from users WHERE id=?"
        result = cursor.execute(find_user,(_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None        
        connection.close()
        return user