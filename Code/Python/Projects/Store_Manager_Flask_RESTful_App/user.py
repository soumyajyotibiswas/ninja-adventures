import sqlite3
from time import sleep
from flask_restful import Resource,request

class User:
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect("data.db", isolation_level=None)
        cursor = sqlite3.connect("data.db")
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
        connection = sqlite3.connect("data.db",isolation_level=None)
        cursor = sqlite3.connect("data.db")
        find_user = "SELECT * from users WHERE id=?"
        result = cursor.execute(find_user,(_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None        
        connection.close()
        return user

class UserRegister(Resource):
    def post(self):
        connection = sqlite3.connect("data.db", isolation_level=None)
        cursor = connection.cursor()
        data=request.get_json()
        username=data['username']
        password=data['password']
        if User.find_by_username(username) == None:
            query = "INSERT INTO users VALUES(NULL, ?, ?);"
            cursor.execute(query,(username,password))
            connection.commit()
            connection.close()
            return {"message":f"User {username!r} created successfully"},201
        else:
            connection.commit()
            connection.close()
            return {"message":f"User {username!r} already exists, the operation is not permitted"},403