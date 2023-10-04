from src.GraphGenerator.graphsgenerator import graph_generator,graph_generator_16,graph_generator_17_18


def graph_redirector(Table,GraphName,result):
    """
    The code helps in redirecting to the correct graph with respect to the graph namme and the table name
    
    """
    if Table == "claimsDeepDive":
        if GraphName in ["LPP_Claims","Prompt_Pay","Adj Reason","Population_Volume","Provider_Status","Funding_ID","LPP_Claims","Prompt_Pay","State","Provider","Group","SubGroup","LOB","Member","Adj_Reason"]:
            response=graph_generator(result,GraphName)
        elif GraphName =="Trend_Analysis_Claims_Volumes":
            response=graph_generator_16(result,GraphName)
        else:
            response=graph_generator_17_18(result,GraphName)

    elif Table=="deep_dive_diag_cds":
        if GraphName in ["Top_10_Procedure_Codes","Top_10_Revenue_Codes","Top_10_Diagnosis_Codes"]:
            
            response==graph_generator(result,GraphName)
    elif Table == "AllAppealsDashboard":
        if  GraphName in ["Outcome_Percentage", "Appeal_Requests", "Summary", "Top_10_Appeal_Reasons","Trend_for_month_of_Appeal_entry_dt"]:
            response = None
    return response

    

if __name__ == "__main__":
    graph_redirector()