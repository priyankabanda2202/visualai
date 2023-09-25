import openai
def get_insight(data, query):
    data =data
    dict1={"Country":"Country","Population_Volume":"clm_its_host_cd_ori","Provider_Status":"in_out_ntwk_cd_ori","Funding_ID":"fundg_cf_lvl_3_desc_ori","State":"mbu_cf_state_ori","Provider":"src_billg_prov_nm_ori","Group":"prchsr_org_name_ori","SubGroup":"subgrp_nbr_ori","Member":"hc_id_ori","Top_10 Procedure Codes":"hlth_srvc_cd","Top 10 Revenue Codes":"rvnu_cd","Top 10 Diagnosis Code":"diag_cd","Trend_Analysis_Claims_Volume":"claim_completion_month_adj","Trend_Analysis_Amounts":"claim_completion_month_adj", "LPP_Trend_Analysis_Amount":"claim_completion_month_adj"}

    template = f"""You are a polite and helpful AI assistant \
        read the question from {query} \
        your job is to generate the useful and detailed insight from the input data in few points \
        (Note: Column names should match the keys of the dictionary i.e. {dict1})\
        written in triple backticks \
        Summarize your answer in 50 words

    input:
    '''{data}'''

    Insight:
    """

    response = openai.ChatCompletion.create( model = "gpt3",   messages = [
    {
        "role": "system",
        "content": template
    }
  ],   max_tokens = 100,   frequency_penalty = 0,   presence_penalty = 0)


    return eval(response)["choices"][0]["message"]["content"]