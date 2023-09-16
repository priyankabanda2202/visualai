import openai
import os
from langchain.chat_models import ChatOpenAI
from fastapi import FastAPI
import pandas as pd
from graphredirector import graph_redirector
from sqlquerygenerator import get_sql_query ,get_graphname
import mysql.connector
connection = mysql.connector.connect(user='root', password='Mysql@123', host='10.189.108.234', database='visualai')


os.environ["REQUESTS_CA_BUNDLE"] = 'root.pem' #Download root.pem from this page and pass it to your code.
openai.api_key = 'LLMal64985FRoGa-/@GLD' #Personalized secured tokenID
openai.api_base = "https://perf-dsmbrsvc.anthem.com/llmgateway/openai" #LLM Gateway designated baseurl.pass the URL as it is.
os.environ['OPENAI_API_KEY'] = 'LLMal64985FRoGa-/@GLD' 
app = FastAPI()
llm = ChatOpenAI(model_name="gpt3", temperature = 0)
@app.get("/")
def home_page():
    return "Welcome to the VisualAI Dashboard using LLM"
@app.get("/visualai")
def get_response(query:str):
    sql_query,Table,graph_name = get_sql_query(query)
    result = pd.read_sql(sql_query, con=connection)
    result=graph_redirector(Table,get_graphname(query),result)
    print(result)
    return result

# llm = ChatOpenAI(model_name="gpt3", temperature = 0)
# text=user_prompt=query ="Show Population_Volume details"


# sql_query,Table,graph_name = get_sql_query(user_prompt)
# print(sql_query)
# result = pd.read_sql(sql_query, con=connection)

# final_response=graph_redirector(Table,get_graphname(user_prompt),result)
# print(final_response)

        
