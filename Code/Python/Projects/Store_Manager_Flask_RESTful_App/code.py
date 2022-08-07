from flask import Flask
from flask_restful import Resource, Api, request
from typing import Union, Dict, List, Type, Any
from flask_jwt import JWT, jwt_required
from security import authenticate,identity

json_type=Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
app = Flask(__name__)
app.secret_key = 'TopSecretKey'
api = Api(app)
jwt = JWT(app,authenticate,identity)

# In memory database
stores=[
    {
        "name": "Store_1",
        "items": [
            {
                "name": "Item_1",
                "price": 1.1
            }
        ]
    },
    {
        "name": "Store_2",
        "items": [
            {
                "name": "Item_1",
                "price": 1.1
            },
            {
                "name": "Item_2",
                "price": 1.2
            }
        ]
    }
]

class Stores(Resource):

    @jwt_required()
    def get(self, all_items:str = None) -> json_type:
        if all_items != None:
            if all_items == 'all':
                return {"items":stores}
            else:
                return {"items": []}, 404
        return {"stores":[store['name'] for store in stores]}

    def put(self) -> json_type:
        request_data = request.get_json()
        if request_data['name'] in [store['name'] for store in stores]:
            return {"message": f"Cannot create store {request_data['name']!r} which is already present."}, 403
        stores.append({"name": request_data['name'], "items": []})
        return {"message": f"{request_data['name']!r} created successfully."}, 201

    def delete(self)-> json_type:
        request_data = request.get_json()
        store_name = request_data['name']
        if store_name not in [store['name'] for store in stores]:
            return {"message": f"Cannot delete store {store_name!r} which is not present."}, 403
        elif len([store['items'] for store in stores if store['name']==store_name][0]) > 0:
            return {"message": f"Cannot delete store {store_name!r} which is not empty."}, 403
        current_store = [store for store in stores if store['name']==store_name][0]
        stores.remove(current_store)
        return {"message": f"{store_name!r} deleted successfully."}

api.add_resource(Stores, '/stores', endpoint="stores")
api.add_resource(Stores, '/stores/<string:all_items>', endpoint="all_items_all_stores")
api.add_resource(Stores, '/stores/create', endpoint="create_store")
api.add_resource(Stores, '/stores/delete', endpoint="delete_store")

class Store(Resource):

    @jwt_required()
    def get(self,store_name: str,item_name: str=None)-> json_type:

        # Check if store name is valid
        if store_name not in [store['name'] for store in stores]:
            return {"message":f"{store_name!r} not found."}, 404

        # Find the current store inventory
        current_store = [store for store in stores if store['name']==store_name][0]

        # Return all items if requested
        if item_name == 'all':
            return {"items": current_store['items']}
        
        # Return only single item if in inventory
        if item_name not in [item['name'] for item in current_store['items']]:
            return {"message": f"{item_name!r} not found in store {store_name!r}."}, 404
        else:
            return {"item": [item for item in current_store['items'] if item['name']==item_name][0]}
        
    def put(self,store_name: str,item_name: str=None)-> json_type:
        
        request_data = request.get_json()
        item_price = request_data['price']

        # Check if store name is valid
        if store_name not in [store['name'] for store in stores]:
            return {"message":f"{store_name!r} not found."}, 404

        # Find the current store inventory
        current_store = [store for store in stores if store['name']==store_name][0]

        if item_name == 'all':
            return {"message":f"{item_name!r} name is not allowed."}, 403

        # Create / Update item
        if item_name not in [item['name'] for item in current_store['items']]:
            current_store['items'].append({"name":item_name,"price":item_price})
        else:
            [item for item in current_store['items'] if item['name']==item_name][0]['price']=item_price
        return {"message": f"{item_name!r} of price {item_price!r} added to store {store_name!r}."}, 201

    def delete(self,store_name: str,item_name: str=None)-> json_type:

        # Check if store name is valid
        if store_name not in [store['name'] for store in stores]:
            return {"message":f"{store_name!r} not found."}, 404

        # Find the current store inventory
        current_store = [store for store in stores if store['name']==store_name][0]

        # Delete item
        if item_name not in [item['name'] for item in current_store['items']]:
            return {"message":f"{item_name!r} not found in {store_name!r}."}, 404
        else:
            current_store['items'].remove([item for item in current_store['items'] if item['name']==item_name][0])
        return {"message": f"{item_name!r} deleted from store {store_name!r}."}

api.add_resource(Store, '/stores/store/<string:store_name>/item/<string:item_name>')

class Home(Resource):
    def get(self):
        return "Welcome to store manager api program."

api.add_resource(Home, '/')

# Run app
app.run(port=5000)