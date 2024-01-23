from utilities import split_schema, execute_python_code
import psycopg2
import logging

class PostgreSqlDb:
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
        
        #proof of concept with ZERO security in mind
        #TODO: handle credentials properly
        self._connection = psycopg2.connect(dbname='postgres', user="postgres", password="admin", host="localhost")
        self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = self._connection.cursor()

        try:
            cursor.execute("DROP DATABASE IF EXISTS postgre_temp_db;")
            cursor.execute("CREATE DATABASE postgre_temp_db;")
        except Exception as e:
            logging.critical("Failed to create PostGreSql database:", e)

        self._connection.close()
        self._connection = psycopg2.connect(dbname='postgre_temp_db', user='postgres', password='admin', host='localhost')
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._structure)
        except Exception as e:
            logging.critical("Failed to create PostGreSql database: {}".format(e))

        try:
            cursor.execute(self._inserts)
        except Exception as e:
            logging.critical("Failed to add data to PostGreSql database: {}".format(e))

        try:
            execute_python_code(self._custom_code, self._connection)
        except Exception as e:
            logging.critical("Failed to execute custom script(postgre) {}".format(e))

        # attempting to reset connection before queries
        self._connection.close()
        self._connection = psycopg2.connect(dbname='postgre_temp_db', user='postgres', password='admin', host='localhost')

