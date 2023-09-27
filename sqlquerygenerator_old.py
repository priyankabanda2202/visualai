import openai
import os
import patch
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
os.environ["REQUESTS_CA_BUNDLE"] = 'root.pem' #Download root.pem from this page and pass it to your code.
openai.api_key = 'LLMal64985FRoGa-/@GLD' #Personalized secured tokenID
openai.api_base = "https://perf-dsmbrsvc.anthem.com/llmgateway/openai" #LLM Gateway designated baseurl.pass the URL as it is.

os.environ['OPENAI_API_KEY'] = 'LLMal64985FRoGa-/@GLD' 

llm = ChatOpenAI(model_name="gpt3", temperature = 0)
# patch.monkey_patch()
#patch.replace_line(r'C:\ProgramData\Anaconda3\envs\venv\Lib\site-packages\langchain\chat_models\openai.py', 362, '        for res in eval(response)["choices"]:\n')
#patch.replace_line(r'C:\ProgramData\Anaconda3\envs\venv\Lib\site-packages\langchain\chat_models\openai.py', 369, '        token_usage = eval(response).get("usage", {})\n')
#patch.call_monkey_patch()
template_dict = {
    #graph 1,2,3,5,6,7,8,9,10,11,13,14,15
    "template_1" : """
        Write a SQL Query which queries the column name and the count given the table name {Table} and columns as a list {Columns} for the given question : 
        {question}.

        """ ,
    #gaph 17
    "template_2" : """
         Write a SQL Query which queries the date and column name  and the sum of columns as a list {Columns} on the given the table name {Table} and  for the given question : 
        {question2}.
    
        if date is there, then the query should return with group by date : {date}.
        """,
    #graph 18
    "template_3" : """
        SELECT claim_completion_month_adj,SUM(intrst_amt_adj),
        SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj!=table.clm_rcvd_dt_adj,Intrst_Amt_Adj,0)) AS PROMPT_Pay_LPP_Correct_Amt,
        SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj=table.clm_rcvd_dt_adj,Intrst_Amt_Adj,0)) AS Prompt_Pay_LPP_Error_Amt FROM claimsDeepDive GROUP BY claim_completion_month_adj
    """,
    #graph 16
    "template_4" : """
        SELECT claim_completion_month_adj,SUM(intrst_amt_adj),
        SUM(IF(claimsDeepDive. prompt_pay_adj = 'Yes',1,0)) AS Prompt_pay_claims,
        SUM(IF(claimsDeepDive. prmpt_pay_clm_rcvd_dt_adj = claimsDeepDive. clm_rcvd_dt_adj, Clm Nbr,NULL)) AS Claims_LPP_Error_Amt,
        SUM(IF(claimsDeepDive. prmpt_pay_clm_rcvd_dt_adj != claimsDeepDive. clm_rcvd_dt_adj, Clm Nbr,NULL)) AS Claims_LPP_Correct_Amt,
        COUNT(Clm_Nbr) as Number_of_Total_Claims
        FROM claimsDeepDive 
        GROUP BY claim_completion_month_adj""",
    # graph 12
    "template_5" : """
        Write a SQL Query which queries the column name and the count group by {graph_name} given the table name {Table} and columns as a list {Columns} for the given question : 
        {question}. For multiple column concatenate column as {graph_name} 
    """
}

table_dict = {
    "table_1" : "deep_dive_proc_cds.csv",
    "table_2" : "deep_dive_rvnu_cds.csv",
    "table_3" : "deep_dive_diag_cds.csv",
    "table_4" : "claimsDeepDive"
}

graph_attributes_dict = {
    # Chart 1:
    "Population_Volume" : {
        "template" : template_dict["template_1"],
        "column" : ["clm_its_host_cd_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
        "input_parameters" : "",
    },
    # Chart 2:
    "Provider_Status" : {
        "template" : template_dict["template_1"],
        "column" : ["in_out_ntwk_cd_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
        "input_parameters" : "",
    },
    # Chart 3:
    "Funding_ID" : {
        "template" : template_dict["template_1"],
        "column" : ["fundg_cf_lvl_3_desc_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
        "input_parameters" : "",
    },
    # Chart 4:
    "LPP_Claims" : {
         "SQL_Query" :  '''
        SELECT 
        IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj = claimsDeepDive.clm_rcvd_dt_adj, "LPP Dt = RCVD Dt" , "LPP Dt > RCVD Dt") 
        as LPP_Date_vs_Clm_RCVD_Date, COUNT(*)
        From claimsDeepDive
        Group by LPP_Date_vs_Clm_RCVD_Date;
    '''
    },
    # Chart 5:
    "Prompt_Pay" : {
        "template" : template_dict["template_1"],
        "column" : ["prompt_pay_adj"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 6:
    "State" : {
        "template" : template_dict["template_1"],
        "column" : ["mbu_cf_state_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 7:
     "Provider" : {
        "template" : template_dict["template_1"],
        "column" : ["src_billg_prov_nm_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 8:
    "Group" : {
        "template" : template_dict["template_1"],
        "column" : ["prchsr_org_name_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 9:
    "SubGroup" : {
        "template" : template_dict["template_1"],
        "column" : ["subgrp_nbr_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 10:
    "LOB" : {
        "SQL_Query" :  '''
SELECT  COUNT(*) as COUNT_Number_of_Total_Claims, fncl_mbu_lvl_5_desc_ori * 100 / t.s AS `%_of_claims`
FROM claimsDeepDive
CROSS JOIN (SELECT SUM(fncl_mbu_lvl_5_desc_ori) AS s FROM claimsDeepDive) t
group by zone_desc_ori;
'''
    },
    # Chart 11:
     "Member" : {
        "template" : template_dict["template_1"],
        "column" : ["hc_id_ori"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 12:
    "Adj_Reason" : {
        "SQL_Query" :  '''
SELECT CONCAT(claimsDeepDive.src_adjstmnt_rsn_cd_ori, ' ', claimsDeepDive.src_adjstmnt_rsn_desc_ori) AS Adj_Reason, 
COUNT(*) AS COUNT 
FROM claimsDeepDive 
GROUP BY Adj_Reason;
    '''
    },
    # Chart 13:
    "Top_10_Procedure_Codes" : {
        "template" : template_dict["template_1"],
        "column" : ["hlth_srvc_cd"],
        "table" : table_dict["table_1"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 14:
    "Top_10_Revenue_Codes" : {
        "template" : template_dict["template_1"],
        "column" : ["rvnu_cd"],
        "table" : table_dict["table_2"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 15:
     "Top_10_Diagnosis_Codes" : {
        "template" : template_dict["template_1"],
        "column" : ["diag_cd"],
        "table" : table_dict["table_3"],
        "input_variables" : ["Table","question","Columns"],
    },
    # Chart 16:
    "Trend_Analysis_Claims_Volumns" : {
        "SQL_Query" :  """SELECT claim_completion_month_adj,
SUM(intrst_amt_adj),    
SUM(IF(claimsDeepDive.prompt_pay_adj = 'Yes',1,0)) AS Prompt_pay_claims,     
SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj = claimsDeepDive.clm_rcvd_dt_adj,1,NULL)) AS Claims_LPP_Error_Amt,     
SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj != claimsDeepDive.clm_rcvd_dt_adj, 1,NULL)) AS Claims_LPP_Correct_Amt,     
COUNT(*) as Number_of_Total_Claims     
FROM claimsDeepDive      
GROUP BY claim_completion_month_adj"""
    },
    # Chart 17:
    "Trend_Analysis_Amounts" : {
        "template" : template_dict["template_2"],
        "column" : ["paid_amt_adj", "totl_chrg_amt_adj", "intrst_amt_adj"],
        "table" : table_dict["table_4"],
        "input_variables" : ["Table","question2","Columns","date"],
    },
    # Chart 18:
    "LPP_Trend_Analysis_Amounts" : {
        "SQL_Query" :  """SELECT claim_completion_month_adj,SUM(intrst_amt_adj),
    SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj!=claimsDeepDive.clm_rcvd_dt_adj,Intrst_Amt_Adj,0)) AS PROMPT_Pay_LPP_Correct_Amt,
    SUM(IF(claimsDeepDive.prmpt_pay_clm_rcvd_dt_adj=claimsDeepDive.clm_rcvd_dt_adj,Intrst_Amt_Adj,0)) AS Prompt_Pay_LPP_Error_Amt FROM claimsDeepDive GROUP BY claim_completion_month_adj
    """
    }    
}

def get_graphname(query):

    template = """
    What is the intent of the following input {query},

    Give your answer as a single word from the below intent list else answer should be None \
    Population_Volume \
    Provider_Status \
    Funding_ID \
    LPP_Claims \
    Prompt_Pay \
    State \
    Provider \
    Group \
    SubGroup \
    LOB \
    Member \
    Adj_Reason \
    Top_10_Procedure_Codes \
    Top_10_Revenue_Codes \
    Top_10_Diagnosis_Codes \
    Trend_Analysis_Claims_Volumes \
    Trend_Analysis_Amounts \
    LPP_Trend_Analysis_Amounts

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


def get_graph_attributes(graph_name):
    template = graph_attributes_dict[graph_name]["template"];
    input_variables = graph_attributes_dict[graph_name]["input_variables"];
    Table = graph_attributes_dict[graph_name]["table"];
    Columns = graph_attributes_dict[graph_name]["column"];   
    print(template)
    return((template,input_variables,Table,Columns))


def get_sql_query(user_prompt, filter):
    graph_name = get_graphname(user_prompt)
    #print(graph_name)
       
    if graph_name == "None":
        return "Invalid input"
    else:
        #print("i am in get_sql_query")
        #print(graph_attributes_dict[graph_name])
        if("template" in graph_attributes_dict[graph_name]):
            
            template, input_variables, Table, Columns = get_graph_attributes(graph_name)
            #print("Table:",Table)
            
            prompt = PromptTemplate(template=template, input_variables=input_variables)
            llm_chain = LLMChain(prompt=prompt, 
                            llm=llm
                            )

            question = f"Query the count of {Columns}"
            question2 = f"Query the date and sum of {Columns}"
            
            if graph_name == "Trend_Analysis_Amounts": 
                date = "claim_completion_month_adj"
                input_parameters = {"Table" : Table,"question2" :question, "Columns" : Columns, "date" : date, "graph_name":graph_name}
            else:
                input_parameters = {"Table" : Table,"question" :question, "Columns" : Columns, "graph_name":graph_name}   
            response= llm_chain.run(input_parameters)
            intercept_resp = response.split("GROUP")         
            # print(filterKeys[0], "++++++++++++filterKeys")
            try:
                filterKeys = list(filter.keys())
                updated_query = intercept_resp[0]+'where '+filterKeys[0]+' IN ('+filter[filterKeys[0]].strip("")+') GROUP'+intercept_resp[1]
            except:
                updated_query = llm_chain.run(input_parameters)
            
            # print(intercept_resp[0]+'where '+filterKeys[0]+' IN ('+filter[filterKeys[0]].strip("")+') GROUP'+intercept_resp[1], "----------response")
            return(replace_newline(updated_query).strip()),Table,graph_name
        else:
            Table="claimsDeepDive"
            sql_query = graph_attributes_dict[graph_name]["SQL_Query"];
            intercept_resp = sql_query.split("Group")
            # print(intercept_resp[0], "intercept_resp +++++++++++")
            try:
                filterKeys = list(filter.keys())
                updated_query = intercept_resp[0]+'where '+filterKeys[0]+' IN ('+filter[filterKeys[0]].strip("")+') GROUP'+intercept_resp[1]
            except:
                updated_query = graph_attributes_dict[graph_name]["SQL_Query"]
            # print(sql_query, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! sql_query")
            return(replace_newline(updated_query).strip()),Table,graph_name