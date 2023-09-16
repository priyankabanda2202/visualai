from pandasai import PandasAI
import pandas as pd
import numpy as np
from pandasai.llm.starcoder import Starcoder
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import sys
app = FastAPI()


@app.get("/")
def home_page():
    return "Welcome to the VisualAI Dashboard using LLM"
@app.get("/visualai")
async def read_csv(prompt:str):
    file_reader = pd.read_excel(r"C:\Users\AL56164\OneDrive - Elevance Health\Desktop\VisualAI\visual_ai_de\api\utils\data\Copy_Claims_UAT_IMSI_Denied_TestData.xlsx",engine = "openpyxl")
    # Create a new LLM instance with the given API token
    llm = Starcoder(api_token="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")
    pandas_ai = PandasAI(llm=llm)
    
    # Read the CSV file
    df = file_reader.apply(lambda x: x.astype(str), axis=1)
    # df = file_reader
    # Ask the user for a question about the data
    # prompt = input("Ask question about the data: ")
    
    # Run the query using the LLM
    result = pandas_ai.run(df, prompt)
    try:
        result = pandas_ai.run(df, prompt).reset_index(allow_duplicates = True)
        result = result.T.drop_duplicates().T
    except:
        response = {"response_desc":prompt,
                        "response_data": "Please try again with the proper prompt1"}
    
    if isinstance(result, str):
        response = {"response_desc":prompt,
                        "response_data": "Please try again with the proper prompt1"}


    elif 'Claims Status' in result.columns and 'Member Market' in result.columns:
        output1 = result.groupby(['Member Market'], as_index = False).count()
        output = result.groupby(['Claims Status'], as_index = False).count()
#         # output2 = result.groupby(['Claim Date'], as_index = False).count()
        if len(output1) == 1:
            claims_status = output['Claims Status'].tolist()
            member = output['Member Market'].tolist()
            # date = output2['Claim Date'].tolist()
            temp_list = []
            for index in range(len(claims_status)):
                dic = {
                        "xvalue":claims_status[index],
                        "yvalue":member[index],
                        "zvalue":None
                    }
                temp_list.append(dic)
        if len(output1) > 1:
            count_group = result.groupby(['Member Market','Claims Status'],as_index = False).size()
            claims_status = count_group['Claims Status'].tolist()
            member = count_group['Member Market'].tolist()
            count = count_group['size'].tolist()

            temp_list = []
            for index in range(len(claims_status)):
                dic = {
                        "xvalue":claims_status[index],
                        "yvalue":count[index],
                        "zvalue":member[index]
                    }
                temp_list.append(dic)
        try:
            print("Response1")
            response = {
                "response_desc":prompt,
                "response_data":{
                "metrics":temp_list,
                "insights":None
            }
        
        }
        except:
            print("Response2")
            response = {"response_desc":prompt,
                        "response_data": "Please try again with the proper prompt2"}
    
        
    elif 'Reason' in result.columns:
        print(result)
        if 'No Prior Auth' in result['Reason'].tolist():
            val = result.loc[result['Reason']== 'No Prior Auth']
            value = val['Claims Status'].tolist()
            for i in value:
                insight = f"common reason for {i} claims is No Prior Auth"
        try:
            print("Response3")
            response = {
            "response_desc":prompt,
            "response_data":{
            "metrics":None,
            "insights":insight
            }
            }
        except:
            print("Response4")
            response = {"response_desc":prompt,
                    "response_data": "Please try again with the proper prompt3"}
            
    elif 'Claims Status' in result.columns and "Member Market" not in result.columns:
        output = result.groupby(['Claims Status'], as_index = False).count()
        print(len(output))
        if len(output) == 1:
            claims_status = output['Claims Status'].tolist()
            # date = output2['Claim Date'].tolist()
            temp_list = []
            for index in range(len(claims_status)):
                dic = {
                        "xvalue":claims_status[index],
                        "yvalue":None,
                        "zvalue":None
                    }
                temp_list.append(dic)
        if len(output) > 1:
            count_group = result.groupby(['Claims Status'],as_index = False).size()
            claims_status = count_group['Claims Status'].tolist()
            count = count_group['size'].tolist()
            temp_list = []
            for index in range(len(claims_status)):
                dic = {
                    "xvalue":claims_status[index],
                    "yvalue":count[index],
                    "zvalue":None
                }
                temp_list.append(dic)
        try:
            response = {
                "response_desc":prompt,
                "response_data":{
                "metrics":temp_list,
                "insights":None
            }
        
        }
        except:
            print("Response2")
            response = {"response_desc":prompt,
                        "response_data": "Please try again with the proper prompt9"}
        
    
    
        
            
        

    
        
            

    #if isinstance(result, pd.DataFrame):
    #    return result.to_json()
    #elif isinstance(result, str):
    #    return {"Response": result}
    # if isinstance(result, np.ndarray):
    #     return result.to_list()
    #else:
        #return str(result)
    print("Response5")
    return response
    
