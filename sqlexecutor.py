from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain. schema.output import LLMResult
from langchain_community.llms import LlamaCpp
from enum import Enum
from plotter import SmartPlotter
import logging


#prompt template is from https://github.com/defog-ai/sqlcoder/blob/main/prompt.md
prompt_template = """
# Task
Generate a SQL-92 compatible query to answer the following question:
`{user_question}`

# Database Schema
The query will run on a SQLite3 database with the following schema:
{table_metadata_string}

# SQL
```
"""

class SQLStates(Enum):
    READY = 1
    IN_STATEMENT = 2
    EXECUTABLE = 3

class SQLSelectExecutionCallBack(BaseCallbackHandler):
    def __init__(self, sql_connection, prompter):
        self.prompter = prompter
        self.sql_connection = sql_connection
        self.reset()

    def reset(self):
        self.sql_statement = ""
        self.collector = ""
        self.state = SQLStates.READY

    def on_llm_end(self, response: LLMResult, **kwargs):
        try:
            cursor = self.sql_connection.cursor()
            logging.debug("\n\nattempting-->\n\n")
            results = cursor.execute(self.sql_statement)
            if results == None:
                results = cursor.fetchall()
            logging.debug("\nAnswer: ")
            bucket = []
            for r in results:
                bucket.append(r)
                logging.debug(r)
            logging.debug("***")
            self.prompter.return_bucket(bucket)
        except Exception as e:
            logging.critical("\n\nfailed--> {} \n\n".format(e))
        
    def on_llm_new_token(self, token: str, **kwargs):
        self.collector = self.collector + token
        if self.state == SQLStates.READY:
            if token.strip() == "SELECT":
                self.state = SQLStates.IN_STATEMENT
                self.sql_statement = self.sql_statement + token
        elif self.state == SQLStates.IN_STATEMENT:
            self.sql_statement = self.sql_statement + token
            if token.strip() == ";":
                self.state = SQLStates.EXECUTABLE


class SqlExecutor:
    def __init__(self, model_path, sql_connection, sql_structure):
        self.plotter = SmartPlotter()
        self.sql_structure = sql_structure
        self.sql_connection = sql_connection
        self.model_path = model_path
        self.user_query = ""
        self.sqlcallback = SQLSelectExecutionCallBack(sql_connection=self.sql_connection, prompter=self)
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler(), self.sqlcallback])
        
        self.llm = LlamaCpp(
            model_path=self.model_path, temperature=0.1,
            max_tokens=2000,
            n_gpu_layers=40,
            callback_manager=callback_manager, verbose=False) 
        
    def return_bucket(self, bucket):
        self.bucket = bucket
     
    def _build_prompt(self):
        prompt = prompt_template.format(user_question=self.user_query, table_metadata_string=self.sql_structure)
        return prompt
    
    def chat(self):
        self._try_count = 1
        while True:
            self.user_query = input("> ")
            if self.user_query == "q" or self.user_query == "quit":
                break
            prompt = self._build_prompt()
            self.llm.invoke(prompt)
            print(self.plotter.plot(self.bucket))
