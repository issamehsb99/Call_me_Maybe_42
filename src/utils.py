from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
from load_fun import functions



def get_prompt(model):
    prompt1 = """ You are a function-calling assistant.
    Your task is to read the user request and choose the correct function to call.
    You must answer ONLY with valid JSON.
    Do not explain.
    Do not add markdown.
    Do not write text before or after the JSON.
    Available functions:"""
    ids= model.encode(prompt1).tolist()[0]
    return ids

def get_fun_id():
    fn = functions()
    add = ""
    l = 1
    fun_name = []
    fun_para = []
    for i in fn:
        fct =f"name :{i.name} his description: {i.description} his arguments {i.parameters} and she return {i.returns}"
        add = add + f"function {l} " + fct + "\n"
        l +=1
        fun_para.append(i.parameters)
        fun_name.append(i.name)
    fun_name_id = [model.encode(f).tolist()[0] for f in fun_name]
    return fun_name_id