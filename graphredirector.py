from graphsgenerator import graph_generator,graph_generator_16,graph_generator_17_18


def graph_redirector(Table,graph_name,result):
    
#     get_sql_query(graph_name)
    if Table == "claimsDeepDive":
        if graph_name in ["LPP_Claims","Prompt_Pay","Adj Reason","Population_Volume","Provider_Status","Funding_ID","LPP_Claims","Prompt_Pay","State","Provider","Group","SubGroup","LOB","Member","Adj_Reason"]:
            response=graph_generator(result,graph_name)
        elif graph_name =="Trend_Analysis_Claims_Volumes":
            response=graph_generator_16(result,graph_name)
        else:
            response=graph_generator_17_18(result,graph_name)



    elif Table=="deep_dive_diag_cds":
        if graph_name in ["Top_10_Procedure_Codes","Top_10_Revenue_Codes","Top_10_Diagnosis_Codes"]:
            
            response==graph_generator(result,graph_name)
    return response