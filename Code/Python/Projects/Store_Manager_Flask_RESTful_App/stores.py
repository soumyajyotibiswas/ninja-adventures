from connections import Connections
from flask_restful import Resource, request
from flask_jwt import jwt_required
from typing import Union, Dict, List, Type, Any, Tuple

json_type=Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

class Stores(Resource):

    def __init__(self) -> None:
        self.database_connections = Connections()

    @jwt_required()
    def get(self, all_items:str = None) -> json_type:
        connection,cursor = self.database_connections.start_connection()
        query = "SELECT * from stores"
        stores = [row[0] for row in cursor.execute(query)]        
        if all_items != None:
            if all_items == 'all':
                items = [row for row in cursor.execute("SELECT * FROM items")]
                self.database_connections.stop_connection(connection)
                return {"items":[{"id":item[0],"name":item[1],"store_name":item[2],"price":item[3]} for item in items]}
            else:
                self.database_connections.stop_connection(connection)
                return {"items": []}, 404
        self.database_connections.stop_connection(connection)
        return {"stores": stores}
    
    def put(self) -> json_type:
        request_data = request.get_json()
        store_name = request_data['name']
        if self.if_store_exists(store_name):
            return {"message": f"Cannot create store {request_data['name']!r} which is already present."}, 403        
        connection,cursor = self.database_connections.start_connection()
        query = "INSERT INTO stores VALUES (?)"
        cursor.execute(query,(store_name,))
        self.database_connections.stop_connection(connection)
        return {"message": f"{store_name!r} created successfully."}, 201

    def delete(self)-> json_type:
        request_data = request.get_json()
        store_name = request_data['name']
        connection,cursor = self.database_connections.start_connection()

        if not self.if_store_exists(store_name):
            self.database_connections.stop_connection(connection)
            return {"message": f"Cannot delete store {store_name!r} which is not present."}, 403

        items_in_store=[row for row in cursor.execute("SELECT * FROM items WHERE store_name=?",(store_name,))]
        if len(items_in_store) > 0:
            self.database_connections.stop_connection(connection)
            return {"message": f"Cannot delete store {store_name!r} which is not empty."}, 403
        
        cursor.execute("DELETE FROM stores WHERE name=?",(store_name,))
        self.database_connections.commit_connection(connection)
        self.database_connections.stop_connection(connection)
        return {"message": f"{store_name!r} deleted successfully."}

    def if_store_exists(self,store: str)-> bool:
        connection,cursor = self.database_connections.start_connection()
        query = "SELECT * from stores WHERE name=?"
        is_store = len([row for row in cursor.execute(query,(store,))])
        self.database_connections.stop_connection(connection)
        if is_store > 0:
            return True
        else:
            return False

class Store(Resource):

    Stores = Stores()
    def __init__(self) -> None:
        self.database_connections = Connections()
        self.stores = Stores()
    
    def get(self,store_name: str,item_name: str=None)-> json_type:

        # Start DB connection
        connection, cursor = self.database_connections.start_connection()

        # Check if store name is valid
        if not self.stores.if_store_exists(store_name):
            return {"message":f"{store_name!r} not found."}, 404

        # Find the current store inventory
        items = [row for row in cursor.execute("SELECT * FROM items WHERE store_name=?",(store_name,))]

        # Stop DB connection
        self.database_connections.stop_connection(connection)

        # Return all items if requested
        if item_name == 'all':
            if len(items) < 1:
                return {"items":[]}
            return {"items":[{"id":item[0],"name":item[1],"store_name":item[2],"price":item[3]} for item in items]}
        
        # Return only single item if in inventory
        if item_name not in [item[1] for item in items]:
            return {"message": f"{item_name!r} not found in store {store_name!r}."}, 404
        else:
            item_to_return = [item for item in items if item[1]==item_name][0]
            return {"item": {"id":item_to_return[0],"name":item_to_return[1],"store_name":item_to_return[2],"price":item_to_return[3]}}
            
        
    def put(self,store_name: str,item_name: str=None)-> json_type:

        connection,cursor = self.database_connections.start_connection()
        request_data = request.get_json()
        item_price = request_data['price']

        # Check if store name is valid
        if not self.stores.if_store_exists(store_name):
            return {"message":f"{store_name!r} not found."}, 404

        if item_name == 'all':
            return {"message":f"{item_name!r} name is not allowed."}, 403

        items = [row for row in cursor.execute("SELECT * FROM items WHERE store_name=?",(store_name,))]

        # Create / Update item
        if item_name not in [item[1] for item in items]:
            cursor.execute("INSERT INTO items VALUES(NULL,?,?,?)",(item_name,store_name,item_price))
        else:
            cursor.execute("UPDATE items SET price=? WHERE name=? AND store_name=?",(item_price,item_name,store_name))
        self.database_connections.commit_connection(connection)
        self.database_connections.stop_connection(connection)
        return {"message": f"{item_name!r} of price {item_price!r} added to store {store_name!r}."}, 201

    def delete(self,store_name: str,item_name: str=None)-> json_type:

        connection,cursor = self.database_connections.start_connection()

        # Check if store name is valid
        if not self.stores.if_store_exists(store_name):
            return {"message":f"{store_name!r} not found."}, 404

        items = [row for row in cursor.execute("SELECT * FROM items WHERE store_name=?",(store_name,))]

        # Delete item
        if item_name not in [item[1] for item in items]:
            return {"message":f"{item_name!r} not found in {store_name!r}."}, 404
        else:
            cursor.execute("DELETE FROM items WHERE name=? AND store_name=?",(item_name,store_name))
        self.database_connections.commit_connection(connection)
        self.database_connections.stop_connection(connection)
        return {"message": f"{item_name!r} deleted from store {store_name!r}."}