from utilities import split_schema, execute_python_code
import os
import sqlite3
import logging

# This class is identical to the postgreSQL class and has been tested. 
# The problem is that the sqlcoder models don't do well to generate Sqlite compatible code

class SqliteDb:
    def __init__(self, schema_file: str):
        self._connection = None
        self._create_temp_db(schema_file)

    def get_sql_structure(self):
        return self._structure

    def get_sql_connection(self):
        return self._connection

    #TODO: Do we really need to delete and rebuild the database each time? Probably not
    def _create_temp_db(self, schema_file: str):
        (self._structure, self._inserts, self._custom_code) = split_schema(schema_file)

        path = "sqlite_temp_db.db"

        if os.path.exists(path):
            os.remove(path)

        self._connection = sqlite3.connect(path)
        cursor = self._connection.cursor()

        try:
            cursor.executescript(self._structure)
        except Exception as e:
            logging.critical("Failed to create SQLite database: {}".format(e))
        
        try:
            cursor.executescript(self._inserts)
        except Exception as e:
            logging.critical("Failed to add data to SQLite database: {}".format(e))

        try:
            execute_python_code(self._custom_code, self._connection)
        except Exception as e:
            logging.critical("Failed to execute custom script (Sqlite) {}".format(e))

        

        

    

