from typing import Union, Dict, List, Type, Any
json_type=Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample store data
stores=[
    {
        'name': 'My Store 1',
        'items': [
            {
                'name': 'My Item 1',
                'price': 15.99
            }
        ]
    }
]

# POST - receive data by server
# GET - send data back by server

# POST /store data:{store_name:}
@app.route('/store',methods=['POST'])
def create_store() -> json_type:
    request_data = request.get_json()
    new_store={'name':request_data['name'],'items':[]}
    stores.append(new_store)
    return jsonify(new_store)

# GET /store data:{name:<store_name>}
@app.route('/store/<string:store_name>')
def get_store(store_name: str) -> json_type:
    for store in stores:
        if store['name'] == store_name:
            return store
    return jsonify({"message":f"{store_name} not found"})

# GET /store
@app.route('/stores')
def get_stores() -> json_type:
    return jsonify({'stores':stores})

# POST /store/<string:name>/item data:{name:<item_name>,price:<price>}
@app.route('/store/<string:store_name>/item',methods=['POST'])
def create_item_in_store(store_name: str) -> json_type:
    request_data = request.get_json()
    for store in stores:
        if store['name'] == store_name:
            new_item={
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({"message":f"{store_name} not found"})

# GET /store/<string:store_name>/item
@app.route('/store/<string:store_name>/items')
def get_items_in_store(store_name: str) -> json_type:
    for store in stores:
        if store['name'] == store_name:
            return jsonify(store['items'])
    return jsonify({"message":f"{store_name} not found"})

# GET /store/<string:store_name>/item/<string:item_name>
@app.route('/store/<string:store_name>/item/<string:item_name>')
def get_item_in_store(store_name: str,item_name: str) -> json_type:
    for store in stores:
        if store['name'] == store_name:
            for item in store['items']:
                if item['name'] == item_name:
                    return jsonify(item)
            return jsonify({"message":f"Item:{item_name} not found"})
    return jsonify({"message":f"Store:{store_name} not found"})

# GET /
@app.route('/')
def home()-> str:
    return "Welcome to the store API program."

app.run(port=5000)