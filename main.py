import openai
import os
import re
from dotenv import load_dotenv
from fastapi import Request, FastAPI
import pandas as pd
from src.GraphGenerator.graphredirector import graph_redirector
# from src.GraphGenerator.graphgeneratorclass import GraphGenerator
import src.MonkeyPatching.patch as patch
from constants.filterQueries import claimCompletionMonthFilter, claimsEditCdAdjFilter, claimsEditCdOriFilter, claimsProcedureCodeFilter, claimsRevenueCodeFilter, claimsDiagnosisCodeFilter, claimsClaimTypeFilter, claimsLOBFilter, claimsProviderFilter, claimsActionCodeFilter, claimsGroupFilter, claimsLOBFundingTypeFilter
from src.SqlGenerator.sqlquerygenerator import get_sql_query
import mysql.connector
from src.SqlGenerator.querypreprocessing import query_preprocessing
from concurrent.futures import ThreadPoolExecutor
import asyncio
import sys
import logging
import yaml
import uvicorn
from uvicorn import Config


logging.basicConfig(filename='./logs/VisualAILogs.txt',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

SqlConnection = mysql.connector.connect(user='root', password='Mysql@123', host='10.189.108.67', database='visualai')
load_dotenv()
os.environ["REQUESTS_CA_BUNDLE"] = os.environ['openai.api_requests_ca_bundles']
os.environ['OPENAI_API_KEY']=openai.api_key = os.environ['openai.api_key']
openai.api_base = os.environ['openai.api_base']
app = FastAPI()

def load_config():
    with open("config/uvicorn.yml","r") as f:
        config = yaml.safe_load(f)
        return config["uvicorn"]
@app.get("/")
async def home_page():
    return "Welcome to the VisualAI Dashboard using LLM"

@app.get("/visualai")
async def get_response(query:str):
    query=query_preprocessing(query)
    logger.info(f"Hey, I am printing the query, {query}")
    sql_query,Table,graph_name = get_sql_query(query, None)
    result = pd.read_sql(sql_query, con=SqlConnection)
    final_response = graph_redirector(Table,graph_name,result)
    return final_response

def modifyQuery(query, range):
    sql_query = query+range+";"
    data = pd.read_sql(sql_query, con=SqlConnection)
    if data.empty:
        data = {"error": "No More records available"}
    return data

@app.get("/visualai/getClaimSCompMonthFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimCompletionMonthFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsEditCdOriFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsEditCdOriFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsEditCdAdjFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsEditCdAdjFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsProcedureCodeFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsProcedureCodeFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsRevenueCodeFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsRevenueCodeFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsDiagnosisCodeFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsDiagnosisCodeFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsClaimTypeFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsClaimTypeFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsLOBFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsLOBFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsProviderFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsProviderFilter, rangeTO)
    return result

@app.get("/visualai/getClaimsActionCodeFilters")
def get_response(query:int =0):
    rangeTO = str(query*30)
    result = modifyQuery(claimsActionCodeFilter, rangeTO)
    return result

@app.post("/visualai")
async def get_response(request: Request):
    logger.info(f"Starting long operation")
    request_params = await request.json()
    query=query_preprocessing(request_params['query'])
    try:
        sql_query,Table,graph_name = get_sql_query(query, request_params['filter'])
    except:
        sql_query,Table,graph_name = get_sql_query(query, None)
    result = pd.read_sql(sql_query, con=SqlConnection)
    final_response = graph_redirector(Table,graph_name,result)
    return final_response

if __name__ == '__main__':
    uvicorn_config = load_config()
    uvicorn.run (
    "main:app",
    # host = uvicorn_config["host"],
    # port = uvicorn_config["port"],
    # reload= uvicorn_config["reload"],
    workers= uvicorn_config["workers"],
    timeout_keep_alive= uvicorn_config["timeout_keep_alive"]
    )