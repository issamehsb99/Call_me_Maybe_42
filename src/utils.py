from llm_sdk import Small_LLM_Model
import json
model = Small_LLM_Model()
from load_fun import functions


# from llm_sdk import Small_LLM_Model
# import json
# model = Small_LLM_Model()
# from load_fun import functions


def get_fun():
    fn = functions()
    add = ""
    l = 0
    fun_name = []
    dic = {}
    for i in fn:
        fct =f"function id = {l}:{i.name}({list(i.parameters.keys())}description: {i.description} his arguments {i.parameters} and she return {i.returns}"
        add += fct + "\n"
        l +=1
        fun_name.append(i.name)
    fun_name_id = [model.encode(f).tolist()[0] for f in fun_name]
    return  fun_name_id , add


def get_fun_id() ->list[int]:
    ids , i  = get_fun()
    i = i
    return ids


def encode_fun():
    id, fun = get_fun()
    id = id
    ids = model.encode(fun).tolist()[0]
    return ids


def get_my_prompt(model):
    prompt1 = """ You are a function-calling assistant.
    Your task is to read the user request and choose the correct function to call.
    You must answer ONLY with valid JSON.
    Do not explain.
    Do not add markdown.
    Do not write text before or after the JSON.
    give me  id from available functions:"""
    ids = model.encode(prompt1).tolist()[0]
    ids += encode_fun()
    return ids

# print(model.decode(get_my_prompt(model)))
def get_user_prompt() ->list[str]:
    with open("/kaggle/input/datasets/issamhasbi/input-data/function_calling_tests.json", 'r') as f:
        data = json.load(f)
    li_prompt = []
    for i in data:
        li_prompt.append(i.get("prompt"))
    return li_prompt


# print(model.decode(get_my_prompt(model)))
# def get_user_prompt() ->list[str]:
#     with open("data/input/function_calling_tests.json", 'r') as f:
#         data = json.load(f)
#     li_prompt = []
#     for i in data:
#         li_prompt.append(i.get("prompt"))
#     return li_prompt

