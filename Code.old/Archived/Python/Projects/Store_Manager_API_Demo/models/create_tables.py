from connections import Connections

TABLES=[
    {
        "stores":"CREATE TABLE IF NOT EXISTS stores (name TEXT PRIMARY KEY)"
    },
    {
        "items": "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT SECONDARY KEY, store_name text, price float)"
    },
    {
        "users": "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    }
]

class CreateTables():   

    def create_table():
        database_connections = Connections()
        connection, cursor = database_connections.start_connection()
        for query in [item[key] for item in TABLES for key in item.keys()]:
            cursor.execute(query)
            database_connections.commit_connection(connection)
        database_connections.stop_connection(connection)