import langchain
from langchain import chat_models;
import os
import logging
logging.basicConfig(filename='./logs/VisualAILogs.txt',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

#This function replaces the function line with the required line
def replace_line(file_name):
    lines = open(file_name, 'r').readlines()
    out = open(file_name, 'w')
    for i in lines:
        if i.strip() =="for res in response[\"choices\"]:":
            i=i.strip()
            print("before replacing",i)
            i = i.replace(i, "        for res in eval(response)[\"choices\"]:\n")
            out.writelines(i)
        elif i.strip() =="token_usage = response.get(\"usage\", {})":
            i=i.strip()
            i = i.replace(i, "        token_usage = eval(response).get(\"usage\", {})\n")
            out.writelines(i)
        else:                                    
            out.writelines(i)
    out.close()

def monkey_patch():
    logger.info("Entered the Patching")
    path=chat_models.__path__[0]
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file =='openai.py':
                file = os.path.join(dirpath, file)
                replace_line(file)

monkey_patch()

