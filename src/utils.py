# from .llm_sdk import Small_LLM_Model
import json
# model = Small_LLM_Model()
from .load_fun import functions


def get_fun(self):
    fn = functions()
    add = ""
    
    l = 0
    fun_name = []
    dic = {}
     
    for i in fn:
        params = []
        for k, v in i.parameters.items():
            params.append(f"{k}: {'float' if v['type'] == 'number' else v['type'][:3] }")
        fct =f"{i.name}({', '.join(params)}): {i.description}"
        add += fct + "\n"
        l +=1
        fun_name.append(i.name)
    fun_name_id = [self.model.encode(f).tolist()[0] for f in fun_name]
    return  fun_name_id , add


def get_fun_id(self) ->list[int]:
    ids , i  = get_fun(self)
    i = i
    return ids


def encode_fun(self):
    id, fun = get_fun(self)
    id = id
    ids = self.model.encode(fun).tolist()[0]
    return ids


def get_my_prompt(self):
    prompt2 = """
    find the function that maches the request 
    Rules:
        -Respect float type oblige .
    Available functions:\n"""
    prompt1 = (
        "use brain"
        'Answer Example: {"prompt":"change "MESSI" tolower case","name":"fn_to_lower","parameters":{"name":"MESSI"}}\n'
        'Function Data: '
    )
    ids = self.model.encode(prompt1).tolist()[0]
    ids += encode_fun(self)
    return ids

def get_user_prompt() ->list[str]:
    with open("data/input/function_calling_tests.json", 'r') as f:
        data = json.load(f)
    li_prompt = []
    li_final = []
    for i in data:
        li_prompt.append(i.get("prompt"))
    for pr in li_prompt:
        if "\"" in pr:
            pr = pr.replace("\"", "\'")
        li_final.append(pr)
    return li_final
