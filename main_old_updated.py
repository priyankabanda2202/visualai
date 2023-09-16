import openai
import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from fastapi import FastAPI
import pandas as pd
import mysql.connector
connection = mysql.connector.connect(user='root', password='Mysql@123', host='10.189.108.234', database='visualai')

os.environ["REQUESTS_CA_BUNDLE"] = r"C:\Users\AL56164\Downloads\root.pem" #Download root.pem from this page and pass it to your code.
openai.api_key = 'LLMal64985FRoGa-/@GLD' #Personalized secured tokenID
openai.api_base = "https://perf-dsmbrsvc.anthem.com/llmgateway/openai" #LLM Gateway designated baseurl.pass the URL as it is.

os.environ['OPENAI_API_KEY'] = 'LLMal64985FRoGa-/@GLD'
app = FastAPI()

@app.get("/")
def home_page():
    return "Welcome to the VisualAI Dashboard using LLM"
@app.get("/visualai")
def get_response(query:str):
    result = graph_generator(query)
    return replace_newline(result)


llm = ChatOpenAI(model_name="gpt3")
query ="get the details of Prompt pay"


def get_graphname(query):

    template = """
    What is the intent of the following input {query},

    Give your answer as a single word from the below intent list else answer should be None \
    Population_Volume \
    Provider_Status \
    Funding_ID \
    State \
    Provider \
    Group \
    SubGroup \
    Member \
    Top 10 Procedure Codes \
    Top 10 Revenue Codes \
    Top 10 Diagnosis Code \

    """

    prompt = PromptTemplate(template=template, input_variables=["query"])


    llm_chain = LLMChain(prompt=prompt, 
                            llm=llm
                            )
    response= llm_chain.run({"query":query})
    # print(response)
    return response
def replace_newline(str):
    str = str.replace("\n", " ")
    return str
def get_sqlquery(text):
    graph_name = get_graphname(text)
    dict1={"Population_Volume": {'column': 'clm_its_host_cd_ori', 'Table': 'claimsDeepDive'},"Provider_Status": {'column': 'in_out_ntwk_cd_ori', 'Table': 'claimsDeepDive'},"Funding_ID": {'column': 'fundg_cf_lvl_3_desc_ori', 'Table': 'claimsDeepDive'},"State": {'column': 'mbu_cf_state_ori', 'Table': 'claimsDeepDive'},"Provider":{'column': 'src_billg_prov_nm_ori', 'Table': 'claimsDeepDive'},"Group": {'column': 'prchsr_org_name_ori', 'Table': 'claimsDeepDive'},"SubGroup":{'column': 'subgrp_nbr_ori', 'Table': 'claimsDeepDive'},"Member": {'column': 'hc_id_ori', 'Table': 'claimsDeepDive'},"Top 10 Procedure Codes": {'column': 'hlth_srvc_cd', 'Table': 'claimsDeepDive'},"Top 10 Revenue Codes":{'column': 'rvnu_cd', 'Table': 'claimsDeepDive'},"Top 10 Diagnosis Code": {'column': 'diag_cd', 'Table': 'claimsDeepDive'}}
    graph_name1=["Population_Volume","Provider_Status","Funding_ID","State","Provider","Group","SubGroup","Member","Top 10 Procedure Codes","Top 10 Revenue Codes","Top 10 Diagnosis Code"]
  #dict2={k:dict1[k] for k in graph_name1 if k in dict1}
    if graph_name == "None":
        return "Invalid input"
    elif graph_name in graph_name1:
        print(graph_name)
        l1=[]
        l1.append(graph_name)
        dict2={k:dict1[k] for k in l1 if k in dict1}
        for key,value in dict2.items(): 
            column=dict2[key]['column']
            Table=dict2[key]['Table']
            Table = Table
            Columns = column
            question = f"Query the count of {column}"
            template = """
            Write a SQL Query which queries the column name and the count given the table name {Table} and columns as a list {Columns} for the given question : 
            {question}.

            """

            prompt = PromptTemplate(template=template, input_variables=["Table","question","Columns"])
            llm_chain = LLMChain(prompt=prompt, 
                                    llm=llm
                                    )
            response= llm_chain.run({"Table" : Table,"question" :question, "Columns" : Columns})
            print(response)
            return response,Table
            
def graph_generator(text):
    sql_query,Table = get_sqlquery(text)
    if Table == "claimsDeepDive":
#         query = """select claim_type, count(*)
# from(
# select  if(prmpt_pay_clm_rcvd_dt_adj == clm_rcvd_dt_adj, "LPP_DT = RCVD", "LPP_DT > RCVD") as claim_type
# from claimsDeepDive"""
        result = pd.read_sql(sql_query, con=connection)
    else:
        result = pd.read_csv(r"C:\Users\AL56164\OneDrive - Elevance Health\Desktop\deep_dive_diag_cds.csv")
    # result["COUNT"] = [2,3,4,5]
    graph_name = get_graphname(text)

    dict1={"Country":"Country","Population_Volume":"clm_its_host_cd_ori","Provider_Status":"in_out_ntwk_cd_ori","Funding_ID":"fundg_cf_lvl_3_desc_ori","State":"mbu_cf_state_ori","Provider":"src_billg_prov_nm_ori","Group":"prchsr_org_name_ori","SubGroup":"subgrp_nbr_ori","Member":"hc_id_ori","Top 10 Procedure Codes":"hlth_srvc_cd","Top 10 Revenue Codes":"rvnu_cd","Top 10 Diagnosis Code":"diag_cd"}
    graph_name1=["Country","Population_Volume","Provider_Status","Funding_ID","State","Provider","Group","SubGroup","Member","Top 10 Procedure Codes","Top 10 Revenue Codes","Top 10 Diagnosis Code"]
  #dict2={k:dict1[k] for k in graph_name1 if k in dict1}
    if graph_name == "None":
        return "Invalid input"
    elif graph_name in graph_name1:
        print(graph_name)
        l1=[]
        l1.append(graph_name)
        dict2={k:dict1[k] for k in l1 if k in dict1}
        print(result.columns)
        for key,value in dict2.items():           	
            if value  in result.columns and 'COUNT' in result.columns:
                output1 = result.groupby(['COUNT'], as_index = False).count()
                print(output1)
                output = result.groupby([value], as_index = False).count()
                print(output)
                #output2 = result.groupby(['Claim Date'], as_index = False).count()
                if len(output1) == 1:
                    print("hi i am in o=1")
                    value = output[value].tolist()
                    COUNT = output['COUNT'].tolist()
                    temp_list = []
                    for index in range(len(value)):
                        dic = {
                        "xvalue":value[index],
                        "yvalue":COUNT[index],
                        "zvalue":None
                      }
                        temp_list.append(dic)
                    try:
                        print("Response1")
                        response = {
                              "response_desc":text,
                              "response_data":{
                              "metrics":temp_list,
                              "insights":None
                          }

                      }
                    except:
                        print("Response2")
                        response = {"response_desc":text,
                                      "response_data": "Please try again with the proper prompt2"} 
                if len(output1) > 1:
                    print("hi i am in o>1")
                    count_group = result.groupby(['COUNT',value],as_index = False).size()
                    # count_group = pd.DataFrame(count_group, columns = ['size'], index=count_group.index)
                    # count_group=count_group.reset_index(inplace=True)
                    value = count_group[value].tolist()
                    COUNT = count_group['COUNT'].tolist()
                    count = count_group['size'].tolist()
                    temp_list = []
                    for index in range(len(value)):

                        dic = {
                        "xvalue":value[index],
                        "yvalue":COUNT[index],
                        "zvalue":None
                      }
                        temp_list.append(dic)
                        print(temp_list)
                    try:
                        print("Response1")
                        response = {
                              "response_desc":text,
                              "response_data":{
                              "metrics":temp_list,
                              "insights":None
                          }

                      }
                    except:
                        print("Response2")
                        response = {"response_desc":text,
                                      "response_data": "Please try again with the proper prompt2"}                   
    return response
