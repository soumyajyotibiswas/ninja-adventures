from connections import Connections

class Store_Model:
    
    def __init__(self, store_name) -> None:
        self.name = store_name
    
    @staticmethod
    def if_store_exists(store_name: str)-> bool:
        database_connections = Connections()
        connection,cursor = database_connections.start_connection()
        query = "SELECT * from stores WHERE name=?"
        is_store = len([row for row in cursor.execute(query,(store_name,))])
        database_connections.stop_connection(connection)
        if is_store > 0:
            return True
        else:
            return False