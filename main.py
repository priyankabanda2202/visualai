import openai
import os
import re
from langchain.chat_models import ChatOpenAI
from fastapi import Request, FastAPI
import pandas as pd
from graphredirector import graph_redirector
import patch
from constants.filterQueries import claimCompletionMonthFilter
from sqlquerygenerator import get_sql_query ,get_graphname
# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org mysql-connector-python
import mysql.connector
connection = mysql.connector.connect(user='root', password='Mysql@123', host='10.189.108.234', database='visualai')
# patch.monkey_patch()
#patch.replace_line(file, 362, '        for res in eval(response)["choices"]:\n')
#patch.replace_line(file, 369, '        token_usage = eval(response).get("usage", {})\n')

#patch.call_monkey_patch()
os.environ["REQUESTS_CA_BUNDLE"] = 'root.pem' #Download root.pem from this page and pass it to your code.
openai.api_key = 'LLMal64985FRoGa-/@GLD' #Personalized secured tokenID
openai.api_base = "https://perf-dsmbrsvc.anthem.com/llmgateway/openai" #LLM Gateway designated baseurl.pass the URL as it is.
os.environ['OPENAI_API_KEY'] = 'LLMal64985FRoGa-/@GLD' 
app = FastAPI()

@app.get("/")
def home_page():
    return "Welcome to the VisualAI Dashboard using LLM"
@app.get("/visualai")
def get_response(query:str):
    sql_query,Table,graph_name = get_sql_query(query, None)
    result = pd.read_sql(sql_query, con=connection)
    final_response = graph_redirector(Table,graph_name,result)
    return final_response

@app.get("/visualai/getClaimSCompMonthFilters")
def get_response():
    sql_query = claimCompletionMonthFilter
    result = pd.read_sql(sql_query, con=connection)
    return result

@app.post("/visualai")
async def get_response(request: Request):
    request_params = await request.json()
    try:
        sql_query,Table,graph_name = get_sql_query(request_params['query'], request_params['filter'])
    except:
        sql_query,Table,graph_name = get_sql_query(request_params['query'], None)
    result = pd.read_sql(sql_query, con=connection)
    final_response = graph_redirector(Table,graph_name,result)
    return final_response

# llm = ChatOpenAI(model_name="gpt3", temperature = 0)
# text=user_prompt=query ="Show Trend_Analysis_Amounts details"


# sql_query,Table,graph_name = get_sql_query(user_prompt)
# print(sql_query)
# result = pd.read_sql(sql_query, con=connection)

# final_response=graph_redirector(Table,get_graphname(user_prompt),result)
# print(final_response)

        
