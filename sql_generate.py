import openai
import os

os.environ["REQUESTS_CA_BUNDLE"] = r"C:\Users\AL56164\Downloads\root.pem" #Download root.pem from this page and pass it to your code.
openai.api_key = "LLMal16103f15HV!`GLD" #Personalized secured tokenID
openai.api_base = "https://perf-dsmbrsvc.anthem.com/llmgateway/openai" #LLM Gateway designated baseurl.pass the URL as it is.



os.environ['OPENAI_API_KEY'] = "LLMal16103f15HV!`GLD"


from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt4")

Table = "DTP"
Columns = ["clm_its_host_cd_ori"]
question = "Query the count of clm_its_host_cd_ori"
template = """
Write a SQL Query given the table name {Table} and columns as a list {Columns} for the given question : 
{question}.

"""

prompt = PromptTemplate(template=template, input_variables=["Table","question","Columns"])


llm_chain = LLMChain(prompt=prompt, 
                         llm=llm
                         )
response= llm_chain.run({"Table" : Table,"question" :question, "Columns" : Columns})
print(response)