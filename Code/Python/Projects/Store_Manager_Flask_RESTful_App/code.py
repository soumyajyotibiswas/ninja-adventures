from flask import Flask
from flask_restful import Resource, Api
from typing import Union, Dict, List, Type, Any
from flask_jwt import JWT
from security import authenticate,identity
from user import UserRegister
from create_tables import CreateTables
from stores import Stores, Store

json_type=Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
app = Flask(__name__)
app.secret_key = 'TopSecretKey'
api = Api(app)
jwt = JWT(app,authenticate,identity)

# Create DB tables if not present
CreateTables.create_table()

api.add_resource(Stores, '/stores', endpoint="stores")
api.add_resource(Stores, '/stores/<string:all_items>', endpoint="all_items_all_stores")
api.add_resource(Stores, '/stores/create', endpoint="create_store")
api.add_resource(Stores, '/stores/delete', endpoint="delete_store")

api.add_resource(Store, '/stores/store/<string:store_name>/item/<string:item_name>')

class Home(Resource):
    def get(self):
        return "Welcome to store manager api program."

api.add_resource(Home, '/')
api.add_resource(UserRegister, '/register')

# Run app
app.run(port=5000)