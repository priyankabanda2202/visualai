import openai
import pandas as pd
from insights import get_insight



def graph_generator(result,graph_name):
    text=graph_name
    #data_insight = get_insight(result, text)
    dict1={"LPP_Claims":"LPP_Date_vs_Clm_RCVD_Date","Prompt_Pay":"prompt_pay_adj","Adj_Reason": "Adj_Reason","Population_Volume":"clm_its_host_cd_ori","Provider_Status":"in_out_ntwk_cd_ori","Funding_ID":"fundg_cf_lvl_3_desc_ori","State":"mbu_cf_state_ori","Provider":"src_billg_prov_nm_ori","Group":"prchsr_org_name_ori","SubGroup":"subgrp_nbr_ori","Member":"hc_id_ori","Top_10_Procedure_Codes":"hlth_srvc_cd","Top_10_Revenue_Codes":"rvnu_cd","Top_10_Diagnosis_Code":"diag_cd"}
    graph_name1=["LPP_Claims","Prompt_Pay","Adj_Reason","Population_Volume","Provider_Status","Funding_ID","State","Provider","Group","SubGroup","Member","Top_10_Procedure_Codes","Top_10_Revenue_Codes","Top_10_Diagnosis_Code"]
    dict3={"LOB":["fncl_mbu_lvl_5_desc_ori","zone_desc_ori"]}
    #dict2={k:dict1[k] for k in graph_name1 if k in dict1}
    if graph_name == "None":
        return "Invalid input"
    elif graph_name=="LOB":
        text=graph_name
        data_insight = get_insight(result, text)
        result_list=list(result.columns)
        index_list = [0,1,2]
        result_list = [result_list[i] for i in index_list]
        variables = []
        for i in result_list:
            variables.append(i.replace("_", " "))
        for key,value in dict3.items():
            #print("dict3.items:",dict3.items,"result:",result)
#            if any([x in value for x in result.columns]):
            for index in result.columns.to_list():
                #print("index:",index)
                if "COUNT" in index:
                    flag = index
            output1 = result.groupby([flag], as_index = False).count()
            print("output1:",output1)
            output = result.groupby([value[0]], as_index = False).count()
            output2 = result.groupby([value[1]], as_index = False).count()
            print(output)
            #output2 = result.groupby(['Claim Date'], as_index = False).count()
            if len(output1) == 1:
                print("Hi i am in O=1")
                temp_list = []
                #print("temp_list",temp_list)
                value0 = output[value[0]].tolist()
                value1 = output[value[1]].tolist()
                COUNT = output[flag].tolist()
                print("value",value,COUNT)
                
                for index in range(len(value)):
                    dic = {
                    "xvalue":value0[index],
                    "yvalue":COUNT[index],
                    "zvalue":value1[index]
                    }
                    temp_list.append(dic)
                    #print("temp_list",temp_list)
                try:
                    #print("Response1")
                    response = {
                            "response_desc":text,
                            "response_data":{
                            "metrics":temp_list,
                            "insights":"None"
                        }

                    }
                except:
                    print("Response2")
                    response = {"response_desc":text,
                                    "response_data": "Please try again with the proper prompt2"} 
            if len(output1) > 1:
                print("result in O>1:",result)
                print("Hi i am in O>1")
                count_group = result.groupby([flag,value[0],value[1]],as_index = False).size()
                print("count_group>1:",count_group)
                # count_group = pd.DataFrame(count_group, columns = ['size'], index=count_group.index)
                # count_group=count_group.reset_index(inplace=True)
                value0 = count_group[value[0]].tolist()
                COUNT = count_group[flag].tolist()
                value1 = count_group[value[1]].tolist()
                count = count_group['size'].tolist()
                temp_list = []
                print("count_group:",count_group)
                print("value0:",value0,"value1:",value1,"COUNT:",COUNT)
                for index in range(len(value0)):

                    dic = {
                    "LOB":value0[index],                        
                    "Number of claims":COUNT[index],
                    "Zone":value1[index]
                    }
                    temp_list.append(dic)
                    #print(temp_list)
                    #print("all",temp_list)
                try:
                    #print("Response1")
                    response = {
                            "response_desc":text,
                            "response_data":{
                            "metrics":temp_list,
                            "variables":variables,
                            "insights":data_insight
                        }

                    }
                except:
                    #print("Response2")
                    response = {"response_desc":text,
                                    "response_data": "Please try again with the proper prompt2"}       

    elif graph_name in graph_name1:
        print("hi i am in elif block in  graph_generator_block")
        print(graph_name)
        text=graph_name
        data_insight = get_insight(result, text)
        result_list=list(result.columns)
        print("result_list:",result_list)
        index_list = [0,1]
        result_list = [result_list[i] for i in index_list]
        variables = []
        for i in result_list:
            variables.append(i.replace("_", " "))
        l1=[]
        l1.append(graph_name)
        dict2={k:dict1[k] for k in l1 if k in dict1}
        print(result)
        print(result.columns)
        #print(l1)
        #print(dict2)
        for key,value in dict2.items():           	
            if value  in result.columns:
                for index in result.columns.to_list():
                    if "COUNT" in index:
                        flag = index
                output1 = result.groupby([flag], as_index = False).count()
                #print(output1)
                output = result.groupby([value], as_index = False).count()
                #print(output)
                #output2 = result.groupby(['Claim Date'], as_index = False).count()
                if len(output1) == 1:
                    print("Hi i am in O=1")
                    temp_list = []
                    #print("temp_list",temp_list)
                    value = output[value].tolist()
                    COUNT = output[flag].tolist()
                    #print("value",value,COUNT)
                    
                    for index in range(len(value)):
                        dic = {
                        "xvalue":value[index],
                        "yvalue":COUNT[index],
                        "zvalue":None
                      }
                        temp_list.append(dic)
                        #print("temp_list",temp_list)
                    try:
                        #print("Response1")
                        response = {
                              "response_desc":text,
                              "response_data":{
                              "metrics":temp_list,
                              "insights":"None"
                          }

                      }
                    except:
                        #print("Response2")
                        response = {"response_desc":text,
                                      "response_data": "Please try again with the proper prompt2"} 
                if len(output1) > 1:
                    #print("Hi i am in O>1")
                    count_group = result.groupby([flag,value],as_index = False).size()
                    print("count_group:",count_group)
                    # count_group = pd.DataFrame(count_group, columns = ['size'], index=count_group.index)
                    # count_group=count_group.reset_index(inplace=True)
                    value = count_group[value].tolist()
                    COUNT = count_group[flag].tolist()
                    count = count_group['size'].tolist()
                    print("value0:",value,"COUNT:",COUNT)
                    temp_list = []
                    for index in range(len(value)):

                        dic = {
                        "xvalue":value[index],                        
                        "yvalue":COUNT[index],
                        "zvalue":None
                      }
                        temp_list.append(dic)
                        #print(temp_list)
                        print("all",temp_list)
                        print("text:",text,"variables:",variables,"data_insight:",data_insight)
                    try:
                        print("Response1")
                        
                        response = {
                              "response_desc":text,
                              "response_data":{
                              "metrics":temp_list,
                              "variables":str(variables),
                              "insights":data_insight
                          }

                      }
                    except:
                        #print("Response2")
                        response = {"response_desc":text,
                                     "response_data": "Please try again with the proper prompt2"}  
                                           
    return response
def graph_generator_16(result,graph_name):
    #result=df = pd.read_csv('data-Copy.csv')
    variables = []
    for i in result.columns:
        variables.append(i)
   # data_insight = "None"
   
    text=graph_name
    data_insight = get_insight(result, text)
    result_list=list(result.columns)
    index_list = [1, 2, 3,4,5]
    result_list = [result_list[i] for i in index_list]
    #print("type of result.columns",type(result.columns))
    variables = []
    for i in result_list:
        variables.append(i.replace("_", " "))
    
    #result=df
    #graph_name = text
     
    if graph_name == "None":
        
        
        return "Invalid input"
    else:
        
        output1 = result.groupby([result.columns[0]], as_index = False).count()
    # output2 = result.groupby([result.columns[1]], as_index = False).count()
    # output3= result.groupby([result.columns[2]], as_index = False).count()
    # output4 = result.groupby([result.columns[3]], as_index = False).count()
    #output2 = result.groupby(['Claim Date'], as_index = False).count()
        if len(output1) > 1:
            
                
            
            print("hi i am in o>1")
            count_group = result.groupby([result.columns[0],result.columns[1],result.columns[2],result.columns[3],result.columns[4],result.columns[5]], as_index = False).size()
      #count_group = pd.DataFrame(count_group, columns = ['size'], index=count_group.index)
      #count_group=count_group.reset_index(inplace=True)
            value1 = count_group[result.columns[1]].tolist()
            value2 = count_group[result.columns[2]].tolist()
            value3 = count_group[result.columns[3]].tolist()
            value4 = count_group[result.columns[4]].tolist()
            value5 = count_group[result.columns[5]].tolist()
            DATE = count_group[result.columns[0]].tolist()
            temp_list = []
            if len(value1)==len(value2)==len(value3)==len(value4)==len(value5):
                

                for index in range(len(value1)):
                    
                    dic = {
                    result.columns[1].replace("_", " "):value1[index],
                    result.columns[2].replace("_", " "):value2[index],
                    result.columns[3].replace("_", " "):value3[index],
                    result.columns[4].replace("_", " "):value4[index],
                    result.columns[5].replace("_", " "):value5[index],
                    result.columns[0].replace("_", " "):DATE[index]
                    }
                    temp_list.append(dic)
                    #print("16",temp_list)
                    try:
                        print("Response1")
                        #print(temp_list)
                        response = {
                            "response_desc":text,
                            "response_data":{
                            "metrics":temp_list,
                            "insights":data_insight,
                            "variables":variables
                        }

                    }
                    except:
                        print("Response2")
                        response = {"response_desc":text,
                                        "response_data": "Please try again with the proper prompt2"}          
                        #print(temp_list)
    #print("16",response)                    
    return response
#print(graph_generator_16(result,"Trend_Analysis_Claims_Volumns"))
def graph_generator_17_18(result,graph_name):
    
    text=graph_name
    data_insight = get_insight(result, text)
    print(graph_name)
    result_list=list(result.columns)
    index_list = [1, 2, 3]
    result_list = [result_list[i] for i in index_list]
    #print("type of result.columns",type(result.columns))
    variables = []
    for i in result_list:
        variables.append(i.replace("_", " "))
#   result=df
#   graph_name = text
     
    if graph_name == "None":
        
        return "Invalid input"
    else:
        output1 = result.groupby([result.columns[0]], as_index = False).count()
        # output2 = result.groupby([result.columns[1]], as_index = False).count()
        # output3= result.groupby([result.columns[2]], as_index = False).count()
        # output4 = result.groupby([result.columns[3]], as_index = False).count()
        #output2 = result.groupby(['Claim Date'], as_index = False).count()
        if len(output1) > 1:
            print("hi i am in o>1")
            count_group = result.groupby([result.columns[0],result.columns[1],result.columns[2],result.columns[3]], as_index = False).size()
              #count_group = pd.DataFrame(count_group, columns = ['size'], index=count_group.index)
              #count_group=count_group.reset_index(inplace=True)
            print("column nmae",result.columns[1])
            value1 = count_group[result.columns[1]].tolist()
            value2 = count_group[result.columns[2]].tolist()
            value3 = count_group[result.columns[3]].tolist()
            DATE = count_group[result.columns[0]].tolist()
            temp_list = []
            if len(value1)==len(value2)==len(value3):
                

                for index in range(len(value1)):
                    
                    
                    
                    dic = {
                    result.columns[1].replace("_", " "):value1[index],
                    result.columns[2].replace("_", " "):value2[index],
                    result.columns[3].replace("_", " "):value3[index],
                    result.columns[0].replace("_", " "):DATE[index]
                    }
                    temp_list.append(dic)
                    print("17,18",temp_list)
                    try:
                        
                        #print("Response1")
                        response = {
                            "response_desc":text,
                            "response_data":{
                            "metrics":temp_list,
                            "insights":data_insight,
                            "variables":variables
                        }

                    }
                    except:
                        print("Response2")
                        response = {"response_desc":text,
                                        "response_data": "Please try again with the proper prompt2"}          
    print("17,18",response)
    return response
