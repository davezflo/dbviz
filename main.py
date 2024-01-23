import argparse
import os
from postgredb import PostgreSqlDb
from sqlexecutor import SqlExecutor
import logging

#TODO: There are many places that could use better error handling...

def main():
    logging.basicConfig(level=logging.WARNING)
   
    parser = argparse.ArgumentParser(description="parser")
    parser.add_argument("sql_structure_path", type=str, help="path to the file that contains the sql structure.")
    parser.add_argument("model_path", type=str, help="path to the language model to use.")
    args = parser.parse_args()
    sql_path = os.path.join(os.getcwd(), args.sql_structure_path)
    model_path = os.path.join(os.getcwd(), "models", args.model_path)
    
    pg = PostgreSqlDb(sql_path)
    sqe = SqlExecutor(model_path, pg.get_sql_connection(), pg.get_sql_structure())
    sqe.chat()
    
if __name__ == "__main__":
    main()