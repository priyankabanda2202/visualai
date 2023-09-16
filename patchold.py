import langchain
from langchain import chat_models;
import os



#This function replaces the function line with the required line
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def monkey_patch():
    print("Entered monkey patching") 
    path=chat_models.__path__[0]
    print(path)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:        
            if file =='openai.py':
                #print(file)
                file = os.path.join(dirpath, file)
                replace_line(file, 362, '        for res in eval(response)["choices"]:\n')
                replace_line(file, 369, '        token_usage = eval(response).get("usage", {})\n')
                print("Done with the Patching")















#_replace_re = re.compile("foo")


#replace_line(r'C:\ProgramData\Anaconda3\envs\venv\Lib\site-packages\langchain\chat_models\openai.py', 362, '        for res in eval(response)["choices"]:\n')
#replace_line(r'C:\ProgramData\Anaconda3\envs\venv\Lib\site-packages\langchain\chat_models\openai.py', 369, '        token_usage = eval(response).get("usage", {})\n')

# def monkey_create_chat_result(self,response:Mapping[str,Any])->ChatResult:
#     generations=[]
#     for res in eval(response)["choices"]:
#         message=_convert_dict_to_message(res["message"])
#         gen=ChatGeneration(message,generation_info=dict(finish_reason=res.get("finish_reason")),
#         )
#         generation.append(gen)
#     token_usage = eval(response).get("usage",{})
#     llm_output = {"token_usage":token_usage,"model_name":self.model_name}
#     print("done")
#     return ChatResult(generations=generations,llm_output=llm_output)


# def _monkey_patch():
#         print("Hi entering into loop")

# #        if __name__ =='langchain':
#         openai._create_chat_result=monkey_create_chat_result
#         print("Done with replacing ")
# def call_monkey_patch():
#     _monkey_patch()
# call_monkey_patch()


# import os
# import re
# _replace_re = re.compile("foo")
# for dirpath, dirnames, filenames in os.walk("C:\ProgramData\Anaconda3\envs\venv\Lib\site-packages\langchain\chat_models\"):
#     for file in filenames:
#         file = os.path.join(dirpath, file)
#         tempfile = file + ".temp"
#         with open(tempfile, "w") as target:
#             with open(file) as source:
#                 for line in source:
#                     line = _replace_re.sub("foobar", line)
#                     target.write(line)
#         os.rename(tempfile, file)