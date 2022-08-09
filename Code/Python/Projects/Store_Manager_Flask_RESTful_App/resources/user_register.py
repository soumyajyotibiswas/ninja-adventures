from models.connections import Connections
from models.user_model import UserModel
from flask_restful import Resource,request
from flask_jwt import jwt_required

class UserRegister(Resource):
    
    @jwt_required()
    def post(self):
        database_connections = Connections()
        connection, cursor = database_connections.start_connection()
        data=request.get_json()
        username=data['username']
        password=data['password']
        if UserModel.find_by_username(username) == None:
            query = "INSERT INTO users VALUES(NULL, ?, ?);"
            cursor.execute(query,(username,password))
            connection.commit()
            connection.close()
            return {"message":f"User {username!r} created successfully"},201
        else:
            connection.commit()
            connection.close()
            return {"message":f"User {username!r} already exists, the operation is not permitted"},403