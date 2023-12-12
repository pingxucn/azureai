import urllib, os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import AgentExecutor
# Import things that are needed generically
from langchain.agents import AgentType, initialize_agent
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.utilities import SerpAPIWrapper
import os
from docx import Document
from io import BytesIO
from docx.shared import Pt, Inches
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools import PythonREPLTool
class SqlServer:
    def __init__(self, Server, Database, Username, Password, OPENAI_API_KEY, Model_version,temperature_Num, port=1433,odbc_ver=18, topK=10) -> None:
        
        odbc_conn = 'Driver={ODBC Driver '+ str(odbc_ver) + ' for SQL Server};Server=tcp:' + \
            Server + f',{port};Database={Database};Uid={Username};Pwd={Password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
        params = urllib.parse.quote_plus(odbc_conn)
        self.conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

        db = SQLDatabase.from_uri(self.conn_str)

                
        llm = ChatOpenAI(
            openai_api_key=str(OPENAI_API_KEY) ,
            temperature=temperature_Num,
            model_name=str(Model_version)
        )
        self.toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        self.SQL_PREFIX = """You are an agent designed to interact with a Microsoft Azure SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results using SELECT TOP in SQL Server syntax.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.
        """

        # print(deploy_name)
        self.agent_executor = create_sql_agent(
                llm=llm,
                toolkit=self.toolkit,
                verbose=True,
                prefix=self.SQL_PREFIX, 
                topK = topK,
                agent_executor_kwargs={"return_intermediate_steps": True}
            )
        
    def run(self, text: str):
        return self.agent_executor.invoke({"input": text})



class python_document_server:
    def __init__(self,OPENAI_API_KEY, Model_version,temperature_Num) -> None:
        llm = ChatOpenAI(
            openai_api_key=str(OPENAI_API_KEY) ,
            temperature=temperature_Num,
            model_name=str(Model_version)
        )

        self.agent_executor = create_python_agent(
            llm=llm,
            tool=PythonREPLTool(),
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            agent_executor_kwargs={"handle_parsing_errors": True},
            prefix=
                """You are an agent designed to write python code to create word document with paragraph and pictures and save the document and pictures. Make sure the paragraphs and pictures are in the document.
                Given an input, create a syntactically correct code to run, then look at the results of the code and return the answer.
                Unless the user specifies a specific result of examples they wish to obtain, always limit your code to at most {top_k} results using docx and matplotlib libraries.
                You have access to tools for interacting with the python.
                Only use the below tools. Only use the information returned by the below tools to construct your final answer.
                You MUST double check your code before executing it. If you get an error while executing a code, rewrite the code and try again.

                If the question does not seem related to the visualization and documents, just return "I don't know" as the answer.
                """
        )
    def run(self, text: str):
        return self.agent_executor.run(text)
        